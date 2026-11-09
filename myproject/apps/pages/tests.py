from django.test import TestCase
from django.urls import reverse


class LandingViewTests(TestCase):
    def test_landing_renders(self):
        response = self.client.get(reverse('pages_app:landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
