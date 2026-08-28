from django.db import models
from django.contrib.auth.models import User

class EntityEditHistory(models.Model):
    entity = models.ForeignKey('entities.Entity', on_delete=models.CASCADE, related_name='contributions')
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contributions')
    field_name = models.CharField(max_length=100, help_text="Field modified (e.g. name, description, metadata, tags)")
    previous_value = models.TextField(blank=True, help_text="Previous value before modification")
    new_value = models.TextField(blank=True, help_text="New value after modification")
    reason = models.CharField(max_length=255, blank=True, help_text="Reason for the edit")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Entity Edit History'
        verbose_name_plural = 'Entity Edit Histories'

    def __str__(self):
        editor = self.edited_by.username if self.edited_by else "Anonymous"
        return f"Edit on '{self.entity.name}' [{self.field_name}] by {editor} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

# Alias for backward compatibility if needed
MovieContribution = EntityEditHistory
