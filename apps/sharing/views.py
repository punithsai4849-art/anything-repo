from django.shortcuts import render, get_object_or_404
from apps.reviews.models import Review

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

