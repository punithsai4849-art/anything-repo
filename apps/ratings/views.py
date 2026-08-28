from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.entities.models import Entity
from .models import Rating

@login_required
def rate_entity_view(request, entity_id):
    if request.method == 'POST':
        entity = get_object_or_404(Entity, id=entity_id)
        try:
            score = float(request.POST.get('score', 0))
            if score < 0.5 or score > 5.0:
                messages.error(request, "Rating must be between 0.5 and 5.0")
                return redirect('entity_detail', slug=entity.slug)
                
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                entity=entity,
                defaults={'score': score}
            )
            messages.success(request, f"Rated '{entity.name}' {score}★")
        except ValueError:
            messages.error(request, "Invalid rating score submitted.")
            
        return redirect('entity_detail', slug=entity.slug)
    return redirect('home')

@login_required
def delete_rating_view(request, entity_id):
    if request.method == 'POST':
        entity = get_object_or_404(Entity, id=entity_id)
        Rating.objects.filter(user=request.user, entity=entity).delete()
        messages.info(request, f"Removed your rating for '{entity.name}'")
        return redirect('entity_detail', slug=entity.slug)
    return redirect('home')

# Alias
rate_movie_view = rate_entity_view
delete_movie_rating_view = delete_rating_view
