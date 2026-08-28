from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'content_id', 'reason', 'status', 'reported_by', 'created_at']
    list_filter = ['status', 'reason', 'content_type', 'created_at']
    search_fields = ['content_type', 'details', 'reported_by__username']
    list_editable = ['status']
