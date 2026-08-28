from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.name}"


import uuid

def entity_image_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower() if '.' in filename else 'jpg'
    safe_ext = ext if ext in ['jpg', 'jpeg', 'png', 'webp', 'gif'] else 'jpg'
    return f"entities/{uuid.uuid4().hex}.{safe_ext}"

class Entity(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, db_index=True)
    category = models.ForeignKey('categories.Category', on_delete=models.PROTECT, related_name='entities')
    description = models.TextField(blank=True, help_text="Overview or description of this entity")
    
    # Flexible JSONB metadata for category-specific attributes (release_year, brand, author, location, etc.)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Primary Visual Media
    primary_image = models.ImageField(upload_to=entity_image_upload_path, blank=True, null=True)

    primary_image_url = models.URLField(max_length=500, blank=True, help_text="Direct image URL if remote")
    
    tags = models.ManyToManyField(Tag, related_name='entities', blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_entities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category', 'created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "entity"
            unique_slug = base_slug
            num = 1
            while Entity.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @property
    def image_display_url(self):
        if self.primary_image:
            return self.primary_image.url
        if self.primary_image_url:
            return self.primary_image_url
        return None

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings.exists():
            return None
        return round(sum(r.score for r in ratings) / ratings.count(), 1)

    @property
    def ratings_count(self):
        return self.ratings.count()

    @property
    def reviews_count(self):
        return self.reviews.count()

    @property
    def excerpt(self):
        if self.description:
            if len(self.description) > 160:
                return self.description[:157] + "..."
            return self.description
        return "No description provided yet."


class EntityRelationship(models.Model):
    RELATIONSHIP_TYPES = [
        ('created_by', 'Created by'),
        ('developed_by', 'Developed by'),
        ('directed_by', 'Directed by'),
        ('written_by', 'Written by'),
        ('located_in', 'Located in'),
        ('owned_by', 'Owned by'),
        ('part_of', 'Part of'),
        ('related_to', 'Related to'),
        ('inspired_by', 'Inspired by'),
        ('associated_with', 'Associated with'),
    ]

    source_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='outgoing_relationships')
    target_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='incoming_relationships')
    relationship_type = models.CharField(max_length=100, choices=RELATIONSHIP_TYPES, default='related_to')
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['relationship_type', '-created_at']
        verbose_name = 'Entity Relationship'
        verbose_name_plural = 'Entity Relationships'

    def __str__(self):
        return f"{self.source_entity.name} → [{self.get_relationship_type_display()}] → {self.target_entity.name}"


class EntityMedia(models.Model):
    MEDIA_TYPES = [
        ('primary', 'Primary Image'),
        ('cover', 'Cover / Backdrop'),
        ('gallery', 'Gallery Image'),
        ('reference', 'Reference / Screenshot'),
    ]

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='media_items')
    image = models.ImageField(upload_to='entity_media/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True)
    media_type = models.CharField(max_length=50, choices=MEDIA_TYPES, default='gallery')
    source = models.CharField(max_length=255, blank=True, help_text="Attribution or source")
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def display_url(self):
        if self.image:
            return self.image.url
        return self.image_url or None
