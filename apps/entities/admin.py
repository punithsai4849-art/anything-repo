from django.contrib import admin
from .models import Tag, Entity, EntityRelationship, EntityMedia

class EntityRelationshipInline(admin.TabularInline):
    model = EntityRelationship
    fk_name = 'source_entity'
    extra = 1
    autocomplete_fields = ['target_entity']

class EntityMediaInline(admin.TabularInline):
    model = EntityMedia
    extra = 1

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'average_rating', 'ratings_count', 'reviews_count', 'created_by', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['tags']
    inlines = [EntityRelationshipInline, EntityMediaInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Entity Essentials', {
            'fields': ('name', 'slug', 'category', 'description', 'tags')
        }),
        ('Visual Media', {
            'fields': ('primary_image', 'primary_image_url')
        }),
        ('Flexible Metadata (JSONB)', {
            'fields': ('metadata',)
        }),
        ('Audit & Ownership', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(EntityRelationship)
class EntityRelationshipAdmin(admin.ModelAdmin):
    list_display = ['source_entity', 'relationship_type', 'target_entity', 'created_at']
    list_filter = ['relationship_type', 'created_at']
    search_fields = ['source_entity__name', 'target_entity__name', 'relationship_type']
    autocomplete_fields = ['source_entity', 'target_entity']
