from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'entity', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'entity__name', 'title', 'content']
    autocomplete_fields = ['user', 'entity']
