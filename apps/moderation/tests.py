from django.test import TestCase
from django.contrib.auth.models import User
from apps.moderation.models import Report

class ModerationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reporter', password='password123')

    def test_create_report(self):
        report = Report.objects.create(
            reported_by=self.user,
            content_type='entity',
            content_id=1,
            reason='misinformation',
            details='Inaccurate claims'
        )
        self.assertEqual(report.status, 'pending')
        self.assertEqual(report.reason, 'misinformation')
