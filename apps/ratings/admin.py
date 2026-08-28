from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'entity', 'score', 'created_at', 'updated_at']
    list_filter = ['score', 'created_at']
    search_fields = ['user__username', 'entity__name']
    autocomplete_fields = ['user', 'entity']
