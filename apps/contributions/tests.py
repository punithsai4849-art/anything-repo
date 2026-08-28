from django.test import TestCase
from django.contrib.auth.models import User
from apps.categories.models import Category
from apps.entities.models import Entity
from apps.contributions.models import EntityEditHistory
from apps.contributions.services import record_entity_edits

class ContributionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='contributor', password='password123')
        self.category = Category.objects.create(name='Food', slug='food')
        self.entity = Entity.objects.create(
            name='Pizza Margherita',
            category=self.category,
            description='Old description'
        )

    def test_record_entity_edits_audit_history(self):
        original = {'name': self.entity.name, 'description': 'Old description'}
        new = {'name': self.entity.name, 'description': 'Authentic Neapolitan pizza with San Marzano tomatoes'}
        
        contribs = record_entity_edits(
            self.entity, original, new, self.user, reason="Expanded description"
        )
        self.assertEqual(len(contribs), 1)
        self.assertEqual(contribs[0].field_name, 'description')
        self.assertEqual(contribs[0].previous_value, 'Old description')
        self.assertEqual(contribs[0].reason, 'Expanded description')
