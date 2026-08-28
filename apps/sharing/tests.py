from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.entities.models import Entity
from apps.categories.models import Category
from apps.ratings.models import Rating
from apps.reviews.models import Review

class SharingStudioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testcineast', password='testpassword123')
        self.category = Category.objects.create(name='Tech & Software', slug='tech-software')
        self.entity = Entity.objects.create(
            name='Test App Engine',
            slug='test-app-engine',
            category=self.category,
            description='A versatile open-source cloud computing and application platform.',
            metadata={'release_year': '2024', 'creator': 'Open Source'}
        )
        self.rating = Rating.objects.create(
            user=self.user,
            entity=self.entity,
            score=4.5
        )
        self.review = Review.objects.create(
            user=self.user,
            entity=self.entity,
            rating=self.rating,
            title='Incredible Performance',
            content='Super fast, developer-friendly, and beautifully engineered architecture.'
        )

    def test_share_review_card_view(self):
        url = reverse('share_review_card', kwargs={'review_id': self.review.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test App Engine')
        self.assertContains(response, 'Social Share Card Studio')
        self.assertContains(response, 'shareModal')
        self.assertContains(response, 'btnInstagramStory')
        self.assertContains(response, 'instagramGuideModal')
        self.assertContains(response, 'Letterboxd Cinema')
        self.assertContains(response, 'shareLinkWhatsApp')
        self.assertContains(response, 'shareLinkTwitter')
        self.assertContains(response, 'shareLinkLinkedIn')
        self.assertContains(response, 'shareLinkReddit')
        self.assertContains(response, 'shareLinkTelegram')
        self.assertContains(response, 'shareLinkFacebook')
        self.assertContains(response, 'btnModalCopyLink')
        self.assertContains(response, 'btnModalCopyImg')
        # Verify loading intro overlay is completely gone
        self.assertNotContains(response, 'siteIntroOverlay')

    def test_share_entity_card_view_with_review(self):
        url = reverse('share_entity_card', kwargs={'slug': self.entity.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test App Engine')
        self.assertContains(response, 'shareModal')
        self.assertNotContains(response, 'siteIntroOverlay')

    def test_share_entity_card_view_without_reviews(self):
        # Create an entity with no ratings or reviews
        new_entity = Entity.objects.create(
            name='Solitude Place',
            slug='solitude-place',
            category=self.category,
            description='A tranquil destination for contemplation and deep focus.'
        )
        url = reverse('share_entity_card', kwargs={'slug': new_entity.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Solitude Place')
        self.assertContains(response, 'shareModal')
        self.assertNotContains(response, 'siteIntroOverlay')

    def test_home_page_no_loading_overlay(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Verify intro/loading splash animation was fully removed
        self.assertNotContains(response, 'siteIntroOverlay')
        self.assertNotContains(response, 'dismissIntroOverlay')
        self.assertNotContains(response, 'introCardPop')

    def test_share_card_contains_proxy_image_url(self):
        url = reverse('share_review_card', kwargs={'review_id': self.review.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('share_entity_image', kwargs={'slug': self.entity.slug}))

    def test_entity_image_proxy_no_image_404(self):
        url = reverse('share_entity_image', kwargs={'slug': self.entity.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_entity_image_proxy_ssrf_protection(self):
        # Set malicious / private IP image URL
        self.entity.primary_image_url = 'http://127.0.0.1:8000/private.jpg'
        self.entity.save()
        url = reverse('share_entity_image', kwargs={'slug': self.entity.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
