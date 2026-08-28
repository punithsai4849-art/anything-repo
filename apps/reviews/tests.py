from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from apps.categories.models import Category
from apps.entities.models import Entity
from apps.reviews.models import Review

class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='critic', password='password123')
        self.category = Category.objects.create(name='Apps', slug='apps')
        self.entity = Entity.objects.create(name='Spotify', category=self.category)

    def test_review_creation_and_excerpt(self):
        rev = Review.objects.create(
            user=self.user,
            entity=self.entity,
            title='Incredible music streaming app',
            content='Super fast search and recommendations are unparalleled.'
        )
        self.assertEqual(rev.entity.name, 'Spotify')
        self.assertIn('Super fast', rev.excerpt)

    def test_unique_user_entity_review_constraint(self):
        Review.objects.create(user=self.user, entity=self.entity, content='First review')
        with self.assertRaises(IntegrityError):
            Review.objects.create(user=self.user, entity=self.entity, content='Second review')
