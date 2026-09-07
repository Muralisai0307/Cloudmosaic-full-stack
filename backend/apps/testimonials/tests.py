from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Testimonial

class TestimonialTests(APITestCase):
    def setUp(self):
        self.url = reverse('testimonial-list-create')
        self.approved_testimonial = Testimonial.objects.create(
            name="John Doe", email="john@example.com", service="Dev", rating=5, text="Great", is_approved=True
        )
        self.unapproved_testimonial = Testimonial.objects.create(
            name="Jane Doe", email="jane@example.com", service="Dev", rating=4, text="Good", is_approved=False
        )

    def test_approved_testimonials_returned(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "John Doe")

    def test_new_review_defaults_to_unapproved(self):
        payload = {
            "name": "New User",
            "email": "new@example.com",
            "service": "Design",
            "rating": 5,
            "comment": "Awesome!!! Excellent service."
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_testimonial = Testimonial.objects.get(email="new@example.com")
        self.assertFalse(new_testimonial.is_approved)

    def test_invalid_rating(self):
        payload = {
            "name": "New User",
            "email": "new@example.com",
            "service": "Design",
            "rating": 10,
            "comment": "Awesome!!! Excellent service."
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rating', response.data['errors'])
