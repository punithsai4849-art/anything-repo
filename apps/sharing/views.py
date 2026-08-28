from django.shortcuts import render, get_object_or_404
from apps.reviews.models import Review

def share_card_view(request, review_id):
    review = get_object_or_404(
        Review.objects.select_related('user__profile', 'entity__category', 'rating'),
        id=review_id
    )
    context = {
        'review': review,
        'entity': review.entity,
        'category': review.entity.category,
        'rating': review.rating,
        'author': review.user,
    }
    return render(request, 'sharing/share_card.html', context)
