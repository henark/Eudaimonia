from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import LivingWorld, SmartProfile

User = get_user_model()

class LivingWorldAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_and_filter_living_world_by_category(self):
        """
        Ensure we can create a new living world with a category and filter by it.
        """
        # Create a world with the 'science' category
        url = '/api/worlds/'
        data = {
            'name': 'Test Science World',
            'description': 'A world for testing science.',
            'category': 'science'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], 'science')

        # Create another world with the 'art' category
        data = {
            'name': 'Test Art World',
            'description': 'A world for testing art.',
            'category': 'art'
        }
        self.client.post(url, data, format='json')

        # Filter worlds by the 'science' category
        filter_url = '/api/worlds/?category=science'
        response = self.client.get(filter_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Science World')
