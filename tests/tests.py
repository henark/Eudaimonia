from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core.models import LivingWorld

User = get_user_model()

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_living_world(self):
        """
        Ensure we can create a new living world.
        """
        url = '/api/worlds/'
        data = {
            'name': 'Test World in New App',
            'description': 'A test world.',
            'category': 'other'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
