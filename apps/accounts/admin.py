from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'movies_rated_count', 'reviews_count', 'contributions_count']
    search_fields = ['user__username', 'user__email', 'bio']
