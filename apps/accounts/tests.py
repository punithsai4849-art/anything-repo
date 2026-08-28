from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='film_lover',
            email='lover@example.com',
            password='Password123!'
        )

    def test_user_profile_created_automatically(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user.username, 'film_lover')

    def test_user_login(self):
        login_success = self.client.login(username='film_lover', password='Password123!')
        self.assertTrue(login_success)

    def test_user_registration(self):
        response = self.client.post('/register/', {
            'username': 'new_cinephile',
            'email': 'new@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='new_cinephile').exists())

    def test_rate_limiting_login(self):
        # 10 failed login attempts
        for _ in range(10):
            self.client.post('/login/', {'username': 'film_lover', 'password': 'WrongPassword!'})
        
        # 11th attempt must be throttled with HTTP 429
        blocked_resp = self.client.post('/login/', {'username': 'film_lover', 'password': 'WrongPassword!'})
        self.assertEqual(blocked_resp.status_code, 429)

