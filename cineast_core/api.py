from typing import List, Optional, Dict, Any
from datetime import datetime
from ninja import NinjaAPI, Schema
from ninja.security import django_auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.http import HttpRequest

from apps.categories.models import Category
from apps.entities.models import Tag, Entity, EntityRelationship, EntityMedia
from apps.ratings.models import Rating
from apps.reviews.models import Review
from apps.contributions.models import EntityEditHistory
from apps.contributions.services import record_entity_edits
from apps.moderation.models import Report

import logging

logger = logging.getLogger(__name__)

api = NinjaAPI(
    title="anything... API",
    version="2.0.0",
    description="Universal discovery, rating, review, and opinion platform API for anything..."
)

@api.exception_handler(Exception)
def generic_exception_handler(request, exc):
    logger.error(f"Unhandled exception in API request to {request.path}: {exc}", exc_info=True)
    return api.create_response(request, {"detail": "Internal server error"}, status=500)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class UserRegisterIn(Schema):
    username: str
    email: str
    password: str

class UserLoginIn(Schema):
    username: str
    password: str

class UserOut(Schema):
    id: int
    username: str
    email: str
    bio: Optional[str] = ""
    avatar_url: Optional[str] = None
    entities_rated_count: int
    reviews_count: int
    contributions_count: int

class CategoryOut(Schema):
    id: int
    name: str
    slug: str
    description: str
    icon: str
    entities_count: Optional[int] = 0

class TagOut(Schema):
    id: int
    name: str
    slug: str

class EntityRelationshipOut(Schema):
    id: int
    target_entity_id: int
    target_entity_name: str
    target_entity_slug: str
    relationship_type: str
    relationship_label: str

class EntityListOut(Schema):
    id: int
    name: str
    slug: str
    category_name: str
    category_slug: str
    category_icon: str
    description: str
    excerpt: str
    primary_image_url: Optional[str]
    metadata: Dict[str, Any]
    average_rating: Optional[float]
    ratings_count: int
    reviews_count: int
    tags: List[str]

class EntityDetailOut(Schema):
    id: int
    name: str
    slug: str
    category_id: int
    category_name: str
    category_slug: str
    category_icon: str
    description: str
    metadata: Dict[str, Any]
    primary_image_url: Optional[str]
    average_rating: Optional[float]
    ratings_count: int
    reviews_count: int
    tags: List[str]
    relationships: List[EntityRelationshipOut]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime

class EntityCreateIn(Schema):
    name: str
    category_id: int
    description: Optional[str] = ""
    metadata: Optional[Dict[str, Any]] = {}
    primary_image_url: Optional[str] = ""
    tag_names: Optional[List[str]] = []

class EntityUpdateIn(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    primary_image_url: Optional[str] = None
    tag_names: Optional[List[str]] = None
    reason: Optional[str] = ""

class RelationshipCreateIn(Schema):
    target_entity_id: int
    relationship_type: str

class RatingIn(Schema):
    score: float

class RatingOut(Schema):
    id: int
    user: str
    entity_id: int
    score: float
    updated_at: datetime

class ReviewIn(Schema):
    title: Optional[str] = ""
    content: str
    score: Optional[float] = None

class ReviewOut(Schema):
    id: int
    user: str
    entity_id: int
    entity_name: str
    entity_slug: str
    category_name: str
    title: str
    content: str
    excerpt: str
    rating_score: Optional[float]
    created_at: datetime
    updated_at: datetime

class ContributionOut(Schema):
    id: int
    entity_id: int
    field_name: str
    previous_value: str
    new_value: str
    edited_by: Optional[str]
    reason: str
    created_at: datetime

class ReportIn(Schema):
    content_type: str
    content_id: int
    reason: str
    details: Optional[str] = ""

from cineast_core.ratelimit import check_rate_limit, record_rate_limit_attempt, reset_rate_limit

# ---------------------------------------------------------------------------
# Auth Endpoints
# ---------------------------------------------------------------------------

@api.post("/auth/register", response=UserOut, tags=["Auth"])
def register(request: HttpRequest, payload: UserRegisterIn):
    if check_rate_limit(request, 'api_auth_register', max_attempts=10, timeout=900):
        return api.create_response(request, {"detail": "Too many registration attempts. Please wait 15 minutes."}, status=429)

    if User.objects.filter(username__iexact=payload.username).exists():
        return api.create_response(request, {"detail": "Username already exists"}, status=400)
    if User.objects.filter(email__iexact=payload.email).exists():
        return api.create_response(request, {"detail": "Email already exists"}, status=400)
    
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    reset_rate_limit(request, 'api_auth_register')
    login(request, user)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.profile.bio,
        "avatar_url": user.profile.avatar.url if user.profile.avatar else None,
        "entities_rated_count": 0,
        "reviews_count": 0,
        "contributions_count": 0
    }

@api.post("/auth/login", response=UserOut, tags=["Auth"])
def login_endpoint(request: HttpRequest, payload: UserLoginIn):
    if check_rate_limit(request, 'api_auth_login', max_attempts=10, timeout=900):
        return api.create_response(request, {"detail": "Too many login attempts. Please wait 15 minutes."}, status=429)

    user = authenticate(request, username=payload.username, password=payload.password)
    if not user:
        record_rate_limit_attempt(request, 'api_auth_login', timeout=900)
        return api.create_response(request, {"detail": "Invalid username or password"}, status=401)
    
    reset_rate_limit(request, 'api_auth_login')
    login(request, user)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.profile.bio,
        "avatar_url": user.profile.avatar.url if user.profile.avatar else None,
        "entities_rated_count": user.profile.entities_rated_count,
        "reviews_count": user.profile.reviews_count,
        "contributions_count": user.profile.contributions_count
    }


@api.post("/auth/logout", tags=["Auth"])
def logout_endpoint(request: HttpRequest):
    logout(request)
    return {"detail": "Successfully logged out"}

@api.get("/auth/me", response=UserOut, auth=django_auth, tags=["Auth"])
def me(request: HttpRequest):
    user = request.user
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.profile.bio,
        "avatar_url": user.profile.avatar.url if user.profile.avatar else None,
        "entities_rated_count": user.profile.entities_rated_count,
        "reviews_count": user.profile.reviews_count,
        "contributions_count": user.profile.contributions_count
    }


# ---------------------------------------------------------------------------
# Categories Endpoints
# ---------------------------------------------------------------------------

@api.get("/categories", response=List[CategoryOut], tags=["Categories"])
def list_categories(request: HttpRequest):
    categories = Category.objects.annotate(e_count=Count('entities')).order_by('name')
    return [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "description": c.description,
            "icon": c.icon,
            "entities_count": c.e_count
        }
        for c in categories
    ]

# ---------------------------------------------------------------------------
# Entities Endpoints
# ---------------------------------------------------------------------------

@api.get("/entities", response=List[EntityListOut], tags=["Entities"])
def list_entities(request: HttpRequest, limit: int = 20, category: Optional[str] = None, tag: Optional[str] = None):
    qs = Entity.objects.select_related('category').prefetch_related('tags', 'ratings', 'reviews').all()
    if category:
        qs = qs.filter(category__slug=category)
    if tag:
        qs = qs.filter(tags__slug=tag)
    
    entities = qs[:limit]
    return [
        {
            "id": e.id,
            "name": e.name,
            "slug": e.slug,
            "category_name": e.category.name,
            "category_slug": e.category.slug,
            "category_icon": e.category.icon,
            "description": e.description,
            "excerpt": e.excerpt,
            "primary_image_url": e.image_display_url,
            "metadata": e.metadata,
            "average_rating": e.average_rating,
            "ratings_count": e.ratings_count,
            "reviews_count": e.reviews_count,
            "tags": [t.name for t in e.tags.all()]
        }
        for e in entities
    ]

@api.get("/entities/{slug}", response=EntityDetailOut, tags=["Entities"])
def get_entity(request: HttpRequest, slug: str):
    e = get_object_or_404(
        Entity.objects.select_related('category', 'created_by')
        .prefetch_related('tags', 'ratings', 'reviews', 'outgoing_relationships__target_entity'),
        slug=slug
    )
    relationships = [
        {
            "id": r.id,
            "target_entity_id": r.target_entity.id,
            "target_entity_name": r.target_entity.name,
            "target_entity_slug": r.target_entity.slug,
            "relationship_type": r.relationship_type,
            "relationship_label": r.get_relationship_type_display()
        }
        for r in e.outgoing_relationships.all()
    ]
    return {
        "id": e.id,
        "name": e.name,
        "slug": e.slug,
        "category_id": e.category.id,
        "category_name": e.category.name,
        "category_slug": e.category.slug,
        "category_icon": e.category.icon,
        "description": e.description,
        "metadata": e.metadata,
        "primary_image_url": e.image_display_url,
        "average_rating": e.average_rating,
        "ratings_count": e.ratings_count,
        "reviews_count": e.reviews_count,
        "tags": [t.name for t in e.tags.all()],
        "relationships": relationships,
        "created_by": e.created_by.username if e.created_by else None,
        "created_at": e.created_at,
        "updated_at": e.updated_at
    }

@api.post("/entities", response=EntityDetailOut, auth=django_auth, tags=["Entities"])
def create_entity(request: HttpRequest, payload: EntityCreateIn):
    category = get_object_or_404(Category, id=payload.category_id)
    entity = Entity.objects.create(
        name=payload.name,
        category=category,
        description=payload.description or "",
        metadata=payload.metadata or {},
        primary_image_url=payload.primary_image_url or "",
        created_by=request.user
    )
    if payload.tag_names:
        for t_name in payload.tag_names:
            clean_tag = t_name.strip().lstrip('#')
            if clean_tag:
                tag_obj, _ = Tag.objects.get_or_create(name=clean_tag)
                entity.tags.add(tag_obj)

    return get_entity(request, entity.slug)

@api.patch("/entities/{slug}", response=EntityDetailOut, auth=django_auth, tags=["Entities"])
def update_entity(request: HttpRequest, slug: str, payload: EntityUpdateIn):
    entity = get_object_or_404(Entity, slug=slug)
    original_data = {
        'name': entity.name,
        'description': entity.description,
        'metadata': entity.metadata,
        'primary_image_url': entity.primary_image_url
    }
    
    new_data = payload.dict(exclude_unset=True)
    reason = new_data.pop('reason', '') or "Community edit"
    tag_names = new_data.pop('tag_names', None)
    
    for key, val in new_data.items():
        if hasattr(entity, key) and val is not None:
            setattr(entity, key, val)
    entity.save()

    if tag_names is not None:
        entity.tags.clear()
        for t_name in tag_names:
            clean_tag = t_name.strip().lstrip('#')
            if clean_tag:
                tag_obj, _ = Tag.objects.get_or_create(name=clean_tag)
                entity.tags.add(tag_obj)
    
    record_entity_edits(entity, original_data, new_data, request.user, reason)
    return get_entity(request, entity.slug)

@api.post("/entities/{id}/relationships", auth=django_auth, tags=["Entities"])
def create_relationship(request: HttpRequest, id: int, payload: RelationshipCreateIn):
    source = get_object_or_404(Entity, id=id)
    target = get_object_or_404(Entity, id=payload.target_entity_id)
    rel = EntityRelationship.objects.create(
        source_entity=source,
        target_entity=target,
        relationship_type=payload.relationship_type,
        created_by=request.user
    )
    return {"detail": "Relationship created", "id": rel.id}


@api.get("/entities/{id}/history", response=List[ContributionOut], tags=["Contributions"])
def get_entity_history(request: HttpRequest, id: int):
    entity = get_object_or_404(Entity, id=id)
    contributions = entity.contributions.select_related('edited_by').all()
    return [
        {
            "id": c.id,
            "entity_id": entity.id,
            "field_name": c.field_name,
            "previous_value": c.previous_value,
            "new_value": c.new_value,
            "edited_by": c.edited_by.username if c.edited_by else "Anonymous",
            "reason": c.reason,
            "created_at": c.created_at
        }
        for c in contributions
    ]

# ---------------------------------------------------------------------------
# Ratings & Reviews Endpoints
# ---------------------------------------------------------------------------

@api.post("/entities/{id}/rating", response=RatingOut, auth=django_auth, tags=["Ratings"])
def rate_entity(request: HttpRequest, id: int, payload: RatingIn):
    entity = get_object_or_404(Entity, id=id)
    if payload.score not in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
        return api.create_response(request, {"detail": "Invalid rating score. Must be 0.5 - 5.0 in 0.5 increments"}, status=400)
    
    rating, _ = Rating.objects.update_or_create(
        user=request.user,
        entity=entity,
        defaults={'score': payload.score}
    )
    return {
        "id": rating.id,
        "user": rating.user.username,
        "entity_id": entity.id,
        "score": rating.score,
        "updated_at": rating.updated_at
    }

@api.delete("/entities/{id}/rating", auth=django_auth, tags=["Ratings"])
def delete_rating(request: HttpRequest, id: int):
    Rating.objects.filter(user=request.user, entity_id=id).delete()
    return {"detail": "Rating deleted"}

@api.get("/entities/{id}/reviews", response=List[ReviewOut], tags=["Reviews"])
def list_entity_reviews(request: HttpRequest, id: int):
    entity = get_object_or_404(Entity, id=id)
    reviews = entity.reviews.select_related('user', 'rating', 'entity__category').all()
    return [
        {
            "id": r.id,
            "user": r.user.username,
            "entity_id": entity.id,
            "entity_name": entity.name,
            "entity_slug": entity.slug,
            "category_name": entity.category.name,
            "title": r.title,
            "content": r.content,
            "excerpt": r.excerpt,
            "rating_score": r.rating.score if r.rating else None,
            "created_at": r.created_at,
            "updated_at": r.updated_at
        }
        for r in reviews
    ]

@api.post("/entities/{id}/reviews", response=ReviewOut, auth=django_auth, tags=["Reviews"])
def create_review(request: HttpRequest, id: int, payload: ReviewIn):
    entity = get_object_or_404(Entity, id=id)
    
    rating_obj = None
    if payload.score:
        rating_obj, _ = Rating.objects.update_or_create(
            user=request.user,
            entity=entity,
            defaults={'score': payload.score}
        )
    else:
        rating_obj = Rating.objects.filter(user=request.user, entity=entity).first()

    review, _ = Review.objects.update_or_create(
        user=request.user,
        entity=entity,
        defaults={
            'title': payload.title or "",
            'content': payload.content,
            'rating': rating_obj
        }
    )
    return {
        "id": review.id,
        "user": review.user.username,
        "entity_id": entity.id,
        "entity_name": entity.name,
        "entity_slug": entity.slug,
        "category_name": entity.category.name,
        "title": review.title,
        "content": review.content,
        "excerpt": review.excerpt,
        "rating_score": review.rating.score if review.rating else None,
        "created_at": review.created_at,
        "updated_at": review.updated_at
    }

@api.patch("/reviews/{id}", response=ReviewOut, auth=django_auth, tags=["Reviews"])
def update_review(request: HttpRequest, id: int, payload: ReviewIn):
    review = get_object_or_404(Review, id=id)
    if review.user != request.user and not request.user.is_staff:
        return api.create_response(request, {"detail": "Forbidden"}, status=403)
    
    if payload.title is not None:
        review.title = payload.title
    if payload.content:
        review.content = payload.content
    
    if payload.score is not None:
        rating_obj, _ = Rating.objects.update_or_create(
            user=request.user,
            entity=review.entity,
            defaults={'score': payload.score}
        )
        review.rating = rating_obj
        
    review.save()
    return {
        "id": review.id,
        "user": review.user.username,
        "entity_id": review.entity.id,
        "entity_name": review.entity.name,
        "entity_slug": review.entity.slug,
        "category_name": review.entity.category.name,
        "title": review.title,
        "content": review.content,
        "excerpt": review.excerpt,
        "rating_score": review.rating.score if review.rating else None,
        "created_at": review.created_at,
        "updated_at": review.updated_at
    }

@api.delete("/reviews/{id}", auth=django_auth, tags=["Reviews"])
def delete_review(request: HttpRequest, id: int):
    review = get_object_or_404(Review, id=id)
    if review.user != request.user and not request.user.is_staff:
        return api.create_response(request, {"detail": "Forbidden"}, status=403)
    
    review.delete()
    return {"detail": "Review deleted"}


# ---------------------------------------------------------------------------
# Search & Moderation Endpoints
# ---------------------------------------------------------------------------

@api.get("/search", response=List[EntityListOut], tags=["Search"])
def universal_search(request: HttpRequest, q: str, category: Optional[str] = None):
    qs = Entity.objects.filter(
        Q(name__icontains=q) | 
        Q(description__icontains=q) |
        Q(tags__name__icontains=q)
    ).distinct().select_related('category').prefetch_related('tags', 'ratings', 'reviews')
    
    if category:
        qs = qs.filter(category__slug=category)
        
    entities = qs[:25]
    return [
        {
            "id": e.id,
            "name": e.name,
            "slug": e.slug,
            "category_name": e.category.name,
            "category_slug": e.category.slug,
            "category_icon": e.category.icon,
            "description": e.description,
            "excerpt": e.excerpt,
            "primary_image_url": e.image_display_url,
            "metadata": e.metadata,
            "average_rating": e.average_rating,
            "ratings_count": e.ratings_count,
            "reviews_count": e.reviews_count,
            "tags": [t.name for t in e.tags.all()]
        }
        for e in entities
    ]

@api.post("/reports", tags=["Moderation"])
def submit_report(request: HttpRequest, payload: ReportIn):
    report = Report.objects.create(
        reported_by=request.user if request.user.is_authenticated else None,
        content_type=payload.content_type,
        content_id=payload.content_id,
        reason=payload.reason,
        details=payload.details or ""
    )
    return {"detail": "Report submitted for moderation", "report_id": report.id}
