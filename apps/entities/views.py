from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
import json

from apps.categories.models import Category
from .models import Tag, Entity, EntityRelationship, EntityMedia
from apps.ratings.models import Rating
from apps.reviews.models import Review
from apps.contributions.models import EntityEditHistory
from apps.contributions.services import record_entity_edits

def home_view(request):
    featured_entity = Entity.objects.filter(primary_image_url__isnull=False).exclude(primary_image_url='').first()
    if not featured_entity:
        featured_entity = Entity.objects.first()

    recent_entities = Entity.objects.select_related('category').prefetch_related('tags', 'ratings')[:10]
    popular_entities = Entity.objects.annotate(r_count=Count('ratings')).order_by('-r_count', '-created_at')[:10]
    categories = Category.objects.annotate(e_count=Count('entities')).order_by('name')[:12]
    recent_reviews = Review.objects.select_related('user__profile', 'entity__category', 'rating').order_by('-created_at')[:6]


    show_tour = request.session.pop('show_new_user_tour', False)

    context = {
        'featured_entity': featured_entity,
        'recent_entities': recent_entities,
        'popular_entities': popular_entities,
        'categories': categories,
        'recent_reviews': recent_reviews,
        'show_tour': show_tour,
    }
    return render(request, 'entities/home.html', context)


def entity_list_view(request):
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    sort = request.GET.get('sort', 'newest')
    
    qs = Entity.objects.select_related('category').prefetch_related('tags', 'ratings').all()
    
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        qs = qs.filter(category=selected_category)
        
    selected_tag = None
    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        qs = qs.filter(tags=selected_tag)
        
    if sort == 'rating':
        qs = qs.annotate(avg_r=Avg('ratings__score')).order_by('-avg_r', '-created_at')
    elif sort == 'popular':
        qs = qs.annotate(r_count=Count('ratings')).order_by('-r_count', '-created_at')
    else:
        qs = qs.order_by('-created_at')
        
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.annotate(e_count=Count('entities')).order_by('name')

    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'selected_tag': selected_tag,
        'current_sort': sort,
    }
    return render(request, 'entities/entity_list.html', context)

def universal_search_view(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    
    results = []
    selected_category = None
    
    if query:
        qs = Entity.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().select_related('category').prefetch_related('tags', 'ratings')
        
        if category_slug:
            selected_category = Category.objects.filter(slug=category_slug).first()
            if selected_category:
                qs = qs.filter(category=selected_category)
                
        results = qs[:30]
        
    categories = Category.objects.all().order_by('name')
    
    context = {
        'query': query,
        'results': results,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'entities/search.html', context)

def entity_detail_view(request, slug):
    entity = get_object_or_404(
        Entity.objects.select_related('category', 'created_by')
        .prefetch_related(
            'tags',
            'ratings',
            'reviews__user__profile',
            'reviews__rating',
            'outgoing_relationships__target_entity__category',
            'incoming_relationships__source_entity__category',
            'contributions__edited_by'
        ),
        slug=slug
    )
    
    user_rating = None
    user_review = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, entity=entity).first()
        user_review = Review.objects.filter(user=request.user, entity=entity).first()
        
    reviews = entity.reviews.all().order_by('-created_at')
    contributions = entity.contributions.all().order_by('-created_at')[:20]
    
    # Related entities (same category or shared tags)
    related_entities = Entity.objects.filter(
        category=entity.category
    ).exclude(id=entity.id).prefetch_related('ratings')[:6]
    
    context = {
        'entity': entity,
        'user_rating': user_rating,
        'user_review': user_review,
        'reviews': reviews,
        'contributions': contributions,
        'related_entities': related_entities,
    }
    return render(request, 'entities/entity_detail.html', context)

@login_required
def entity_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category_id')
        description = request.POST.get('description', '').strip()
        primary_image_url = request.POST.get('primary_image_url', '').strip()
        primary_image_file = request.FILES.get('primary_image')
        tag_string = request.POST.get('tags', '').strip()
        
        # Parse dynamic category metadata from form
        metadata = {}
        for key in request.POST:
            if key.startswith('meta_'):
                clean_key = key[5:]
                val = request.POST.get(key, '').strip()
                if val:
                    metadata[clean_key] = val

        if not name or not category_id:
            messages.error(request, "Name and Category are required.")
        if primary_image_file:
            if primary_image_file.size > 5 * 1024 * 1024:
                messages.error(request, "Uploaded image must be under 5MB.")
                return redirect('entity_add')
            try:
                from PIL import Image
                img = Image.open(primary_image_file)
                img.verify()
                primary_image_file.seek(0)
            except Exception:
                messages.error(request, "Invalid or corrupted image file.")
                return redirect('entity_add')

        category = get_object_or_404(Category, id=category_id)
        entity = Entity.objects.create(
            name=name,
            category=category,
            description=description,
            metadata=metadata,
            primary_image_url=primary_image_url,
            primary_image=primary_image_file,
            created_by=request.user
        )

        
        # Tags
        if tag_string:
            tags = [t.strip().lstrip('#') for t in tag_string.split(',') if t.strip()]
            for t_name in tags:
                tag_obj, _ = Tag.objects.get_or_create(name=t_name)
                entity.tags.add(tag_obj)
                
        messages.success(request, f"'{entity.name}' has been added to anything...")
        return redirect('entity_detail', slug=entity.slug)
        
    categories = Category.objects.all().order_by('name')
    return render(request, 'entities/entity_add.html', {'categories': categories})

@login_required
def entity_edit_view(request, slug):
    entity = get_object_or_404(Entity, slug=slug)
    
    if request.method == 'POST':
        original_data = {
            'name': entity.name,
            'description': entity.description,
            'metadata': str(entity.metadata),
            'primary_image_url': entity.primary_image_url
        }
        
        entity.name = request.POST.get('name', '').strip() or entity.name
        entity.description = request.POST.get('description', '').strip()
        new_img_url = request.POST.get('primary_image_url', '').strip()
        if new_img_url:
            entity.primary_image_url = new_img_url
            
        if request.FILES.get('primary_image'):
            entity.primary_image = request.FILES.get('primary_image')
            
        # Parse updated metadata
        updated_meta = dict(entity.metadata)
        for key in request.POST:
            if key.startswith('meta_'):
                clean_key = key[5:]
                val = request.POST.get(key, '').strip()
                if val:
                    updated_meta[clean_key] = val
                elif clean_key in updated_meta:
                    del updated_meta[clean_key]
        entity.metadata = updated_meta
        entity.save()
        
        # Tags update
        tag_string = request.POST.get('tags', '').strip()
        if tag_string:
            entity.tags.clear()
            tags = [t.strip().lstrip('#') for t in tag_string.split(',') if t.strip()]
            for t_name in tags:
                tag_obj, _ = Tag.objects.get_or_create(name=t_name)
                entity.tags.add(tag_obj)
                
        reason = request.POST.get('reason', '').strip() or "Updated entity information"
        new_data = {
            'name': entity.name,
            'description': entity.description,
            'metadata': str(entity.metadata),
            'primary_image_url': entity.primary_image_url
        }
        record_entity_edits(entity, original_data, new_data, request.user, reason)
        
        messages.success(request, f"Updated '{entity.name}'. Thank you for your contribution!")
        return redirect('entity_detail', slug=entity.slug)
        
    categories = Category.objects.all().order_by('name')
    existing_tags = ", ".join(t.name for t in entity.tags.all())
    return render(request, 'entities/entity_edit.html', {
        'entity': entity,
        'categories': categories,
        'existing_tags': existing_tags
    })
