from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

def validate_half_star(value):
    if value not in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
        raise ValidationError(f"{value} is not a valid half-star rating between 0.5 and 5.0")

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    entity = models.ForeignKey('entities.Entity', on_delete=models.CASCADE, related_name='ratings')
    score = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0), validate_half_star],
        help_text="Rating score from 0.5 to 5.0 in 0.5 increments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'entity'], name='unique_user_entity_rating')
        ]
        ordering = ['-updated_at']
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f"{self.user.username} rated {self.entity.name}: {self.score}★"
