from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.product_list_url = reverse('product-list')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

        self.product1 = Product.objects.create(
            name='test_Product_1',
            price=Decimal('99.99'),
            quantity=10
        )
        self.product2 = Product.objects.create(
            name='Test_Product_2',
            price=Decimal('149.99'),
            quantity=5
        )

    def test_list_products(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_product_unauthorized(self):
        data = {
            'name': 'new_Product',
            'price': '199.99',
            'quantity': 15
        }
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_authorized(self):
        token_response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword111'
        })
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'name': 'new_Product',
            'price': '199.99',
            'quantity': 15
        }
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Product.objects.get(name='New Product').price, Decimal('199.99'))

    def test_retrieve_product(self):
        url = reverse('product-detail', args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test_Product_1')
        self.assertEqual(response.data['price'], '99.99')

    def test_update_product_unauthorized(self):
        url = reverse('product-detail', args=[self.product1.id])
        data = {'price': '89.99'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_product_authorized(self):
        token_response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword111'
        })
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('product-detail', args=[self.product1.id])
        data = {'price': '89.99'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(id=self.product1.id).price, Decimal('89.99'))

    def test_delete_product_unauthorized(self):
        url = reverse('product-detail', args=[self.product1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), 2)

    def test_delete_product_authorized(self):
        token_response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword111'
        })
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('product-detail', args=[self.product1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)
