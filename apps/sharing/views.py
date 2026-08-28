from django.shortcuts import render, get_object_or_404
from apps.reviews.models import Review
from apps.entities.models import Entity

def share_card_view(request, review_id):
    review = get_object_or_404(
        Review.objects.select_related('user__profile', 'entity__category', 'rating'),
        id=review_id
    )
    metadata = review.entity.metadata or {}
    year = metadata.get('release_year') or metadata.get('year') or ''
    creator = metadata.get('director') or metadata.get('artist') or metadata.get('author') or metadata.get('brand') or ''

    context = {
        'review': review,
        'entity': review.entity,
        'category': review.entity.category,
        'rating': review.rating,
        'author': review.user,
        'year': str(year) if year else '',
        'creator': str(creator) if creator else '',
    }
    return render(request, 'sharing/share_card.html', context)

def share_entity_card_view(request, slug):
    entity = get_object_or_404(
        Entity.objects.select_related('category'),
        slug=slug
    )
    
    # Try to find a featured/user review if available
    review = None
    if request.user.is_authenticated:
        review = entity.reviews.filter(user=request.user).select_related('user__profile', 'rating').first()
    if not review:
        review = entity.reviews.select_related('user__profile', 'rating').order_by('-created_at').first()

    metadata = entity.metadata or {}
    year = metadata.get('release_year') or metadata.get('year') or ''
    creator = metadata.get('director') or metadata.get('artist') or metadata.get('author') or metadata.get('brand') or ''

    context = {
        'review': review,
        'entity': entity,
        'category': entity.category,
        'rating': review.rating if review else None,
        'author': review.user if review else None,
        'year': str(year) if year else '',
        'creator': str(creator) if creator else '',
        'is_entity_share': True,
    }
    return render(request, 'sharing/share_card.html', context)

