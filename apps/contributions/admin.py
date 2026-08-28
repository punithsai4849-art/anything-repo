from django.contrib import admin
from .models import EntityEditHistory

@admin.register(EntityEditHistory)
class EntityEditHistoryAdmin(admin.ModelAdmin):
    list_display = ['entity', 'field_name', 'edited_by', 'created_at', 'reason']
    list_filter = ['field_name', 'created_at']
    search_fields = ['entity__name', 'edited_by__username', 'field_name', 'previous_value', 'new_value', 'reason']
    readonly_fields = ['entity', 'edited_by', 'field_name', 'previous_value', 'new_value', 'created_at']
    autocomplete_fields = ['entity', 'edited_by']
