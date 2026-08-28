from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam / Commercial advertising'),
        ('harassment', 'Harassment / Hate speech'),
        ('misinformation', 'Misinformation / Fabricated claims'),
        ('personal_info', 'Private personal info (Doxxing)'),
        ('abuse', 'Abuse or offensive content'),
        ('other', 'Other issue'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('dismissed', 'Dismissed'),
        ('resolved', 'Resolved (Action Taken)'),
    ]

    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports')
    content_type = models.CharField(max_length=50, help_text="e.g. entity, review, comment")
    content_id = models.IntegerField(help_text="Primary key of the reported item")
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, default='other')
    details = models.TextField(blank=True, help_text="Explanation from the reporter")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self):
        return f"Report #{self.id} on {self.content_type} #{self.content_id} ({self.get_reason_display()})"
