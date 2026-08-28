from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.categories.models import Category
from apps.entities.models import Tag, Entity, EntityRelationship

class EntityModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.cat_movie, _ = Category.objects.get_or_create(name='Movies', slug='movies', defaults={'icon': ''})
        self.cat_tech, _ = Category.objects.get_or_create(name='Technology', slug='technology', defaults={'icon': ''})




    def test_create_generic_entity_with_jsonb_metadata(self):
        e = Entity.objects.create(
            name='Interstellar',
            category=self.cat_movie,
            description='Space exploration film',
            metadata={'release_year': 2014, 'director': 'Christopher Nolan'},
            created_by=self.user
        )
        self.assertEqual(e.slug, 'interstellar')
        self.assertEqual(e.metadata.get('release_year'), 2014)
        self.assertEqual(e.category.name, 'Movies')

    def test_entity_relationships(self):
        movie = Entity.objects.create(name='Inception', category=self.cat_movie)
        director = Entity.objects.create(name='Christopher Nolan', category=self.cat_movie)
        
        rel = EntityRelationship.objects.create(
            source_entity=movie,
            target_entity=director,
            relationship_type='directed_by'
        )
        self.assertEqual(rel.relationship_type, 'directed_by')
        self.assertIn(director, [r.target_entity for r in movie.outgoing_relationships.all()])
