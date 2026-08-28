from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.entities.models import Entity
from apps.ratings.models import Rating
from .models import Review

@login_required
def create_or_update_review_view(request, entity_id):
    if request.method == 'POST':
        entity = get_object_or_404(Entity, id=entity_id)
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        raw_score = request.POST.get('score')
        
        if not content:
            messages.error(request, "Review content cannot be blank.")
            return redirect('entity_detail', slug=entity.slug)
            
        rating_obj = None
        if raw_score:
            try:
                score_val = float(raw_score)
                rating_obj, _ = Rating.objects.update_or_create(
                    user=request.user,
                    entity=entity,
                    defaults={'score': score_val}
                )
            except ValueError:
                pass
        else:
            rating_obj = Rating.objects.filter(user=request.user, entity=entity).first()
            
        review, created = Review.objects.update_or_create(
            user=request.user,
            entity=entity,
            defaults={
                'title': title,
                'content': content,
                'rating': rating_obj
            }
        )
        if created:
            messages.success(request, f"Your review for '{entity.name}' has been published!")
        else:
            messages.success(request, f"Your review for '{entity.name}' has been updated.")
            
        return redirect('entity_detail', slug=entity.slug)
    return redirect('home')

from django.http import HttpResponseForbidden

@login_required
def delete_review_view(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        if review.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to delete this review.")
            
        slug = review.entity.slug
        review.delete()

        messages.info(request, "Review deleted successfully.")
        return redirect('entity_detail', slug=slug)
    return redirect('home')

# Alias
create_or_update_movie_review_view = create_or_update_review_view
delete_movie_review_view = delete_review_view
