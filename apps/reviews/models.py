from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    entity = models.ForeignKey('entities.Entity', on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(help_text="The full review, perspective, or thoughts")
    rating = models.ForeignKey('ratings.Rating', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'entity'], name='unique_user_entity_review')
        ]
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        title_str = f": {self.title}" if self.title else ""
        return f"Review by {self.user.username} on {self.entity.name}{title_str}"

    @property
    def excerpt(self):
        if len(self.content) > 160:
            return self.content[:157] + '...'
        return self.content
