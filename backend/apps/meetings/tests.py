from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import MeetingRequest

class MeetingTests(APITestCase):
    def setUp(self):
        self.url = reverse('meetings-create')
        self.valid_payload = {
            "service": "Cloud Migration",
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "1234567890",
            "company": "Tech Inc",
            "date": "2026-10-10",
            "time": "14:30",
            "notes": "Looking forward to it."
        }

    def test_valid_submission(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MeetingRequest.objects.count(), 1)

    def test_invalid_email(self):
        payload = self.valid_payload.copy()
        payload['email'] = "invalid-email"
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date_time(self):
        payload = self.valid_payload.copy()
        payload['date'] = "not-a-date"
        payload['time'] = "not-a-time"
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data['errors'])
