from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ContactRequest

class ContactTests(APITestCase):
    def setUp(self):
        self.url = reverse('contact-create')
        self.valid_payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "service": "Cloud Migration",
            "message": "Hello world"
        }

    def test_valid_submission(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactRequest.objects.count(), 1)
        self.assertTrue(response.data['success'])

    def test_invalid_email(self):
        payload = self.valid_payload.copy()
        payload['email'] = "invalid-email"
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContactRequest.objects.count(), 0)

    def test_missing_required_field(self):
        payload = self.valid_payload.copy()
        payload.pop('message')
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data['errors'])
