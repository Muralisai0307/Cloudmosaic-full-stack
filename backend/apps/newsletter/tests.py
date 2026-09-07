from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Subscriber

from django.core.cache import cache

class NewsletterTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse('newsletter-subscribe')
        self.valid_payload = {
            "email": "test@example.com"
        }

    def test_valid_subscription(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscriber.objects.count(), 1)
        self.assertTrue(response.data['success'])

    def test_duplicate_email(self):
        # First subscription
        self.client.post(self.url, self.valid_payload, format='json')
        # Second subscription
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], "You are already subscribed to the newsletter.")
        self.assertEqual(Subscriber.objects.count(), 1)

    def test_invalid_email(self):
        response = self.client.post(self.url, {"email": "not-an-email"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(Subscriber.objects.count(), 0)

    def test_reactivate_subscription(self):
        subscriber = Subscriber.objects.create(email="test@example.com", is_active=False)
        response = self.client.post(self.url, {"email": "test@example.com"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscriber.refresh_from_db()
        self.assertTrue(subscriber.is_active)
