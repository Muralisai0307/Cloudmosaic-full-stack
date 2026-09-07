from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Service

class ServiceTests(APITestCase):
    def setUp(self):
        self.url = reverse('service-list')
        self.active_service = Service.objects.create(
            title="Active Service", 
            icon="icon", 
            description="desc", 
            active=True, 
            display_order=1
        )
        self.inactive_service = Service.objects.create(
            title="Inactive Service", 
            icon="icon", 
            description="desc", 
            active=False, 
            display_order=2
        )

    def test_active_services_returned(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Active Service")

    def test_health_check_endpoint(self):
        health_url = reverse('health-check')
        response = self.client.get(health_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['status'], "healthy")
        self.assertEqual(response.data['data']['database'], "connected")
