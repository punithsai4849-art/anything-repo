from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from apps.categories.models import Category
from apps.entities.models import Entity
from apps.ratings.models import Rating

class RatingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rater', password='password123')
        self.category = Category.objects.create(name='Places', slug='places')
        self.entity = Entity.objects.create(name='Hyderabad', category=self.category)

    def test_rating_creation_and_update(self):
        r, created = Rating.objects.update_or_create(
            user=self.user,
            entity=self.entity,
            defaults={'score': 4.5}
        )
        self.assertTrue(created)
        self.assertEqual(r.score, 4.5)
        self.assertEqual(self.entity.average_rating, 4.5)

    def test_unique_user_entity_rating_constraint(self):
        Rating.objects.create(user=self.user, entity=self.entity, score=5.0)
        with self.assertRaises(IntegrityError):
            Rating.objects.create(user=self.user, entity=self.entity, score=3.0)
