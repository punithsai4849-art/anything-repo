import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower() if '.' in filename else 'jpg'
    safe_ext = ext if ext in ['jpg', 'jpeg', 'png', 'webp', 'gif'] else 'jpg'
    return f"avatars/{uuid.uuid4().hex}.{safe_ext}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def entities_rated_count(self):
        return self.user.ratings.count()

    @property
    def reviews_count(self):
        return self.user.reviews.count()

    @property
    def contributions_count(self):
        return self.user.contributions.count()

    @property
    def entities_created_count(self):
        return self.user.created_entities.count()

    # Aliases
    @property
    def movies_rated_count(self):
        return self.entities_rated_count


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
