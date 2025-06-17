from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class UserViewsTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.user_detail_url = reverse('user_detail')
        self.token_url = reverse('token_obtain_pair')
        
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'password2': 'testpass123',
            'email': 'test@example.com',
            'phone': '+89603234456',
            'birth_date': '2007-01-01'
        }
        
        self.user = User.objects.create_user(
            username='existinguser',
            password='existingpass123',
            email='existing@example.com',
            phone='+89603234456',
            birth_date=date(1990, 1, 1)
        )

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='testuser').email, 'test@example.com')

    def test_register_user_password_mismatch(self):
        self.user_data['password2'] = 'differentpass'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_duplicate_username(self):
        self.user_data['username'] = 'existinguser'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_get_user_detail_unauthorized(self):
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail_authorized(self):
        token_response = self.client.post(self.token_url, {
            'username': 'existinguser',
            'password': 'existingpass123'
        })
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        token = token_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')
        self.assertEqual(response.data['email'], 'existing@example.com')

    def test_update_user_detail(self):
        token_response = self.client.post(self.token_url, {
            'username': 'existinguser',
            'password': 'existingpass123'
        })
        token = token_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        update_data = {
            'phone': '+89603234456',
            'email': 'updated@example.com'
        }
        response = self.client.patch(self.user_detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '+89603234456')
        self.assertEqual(response.data['email'], 'updated@example.com')
