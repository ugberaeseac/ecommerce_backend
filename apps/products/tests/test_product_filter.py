import random
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.products.models import Category, Product

class ProductListFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category_1 = Category.objects.create(name="African Snacks")
        cls.category_2 = Category.objects.create(name="Solar Products")

        for i in range(10):
            Product.objects.create(
                name=f"Plantain Chips {i}",
                description="Crispy sliced plantain snack.",
                price=random.randint(100, 500),
                stock=random.randint(0, 10),
                category=cls.category_1
            )

        for i in range(10):
            Product.objects.create(
                name=f"Solar Lamp {i}",
                description="Portable solar lamp for rural homes.",
                price=random.randint(1000, 5000),
                stock=random.randint(0, 10),
                category=cls.category_2
            )

        cls.product_url = reverse('product-list')

    
    def test_pagination_and_page_size(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 10)

    
    def test_product_filter_by_category(self):
        response = self.client.get(self.product_url, {'category': self.category_1.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for product in response.data['results']:
            self.assertIn("Plantain", product['name'])

    
    def test_product_filter_by_price_range(self):
        response = self.client.get(self.product_url, {'min_price': 100, 'max_price': 500})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for product in response.data['results']:
            self.assertGreaterEqual(float(product['price']), 100)
            self.assertLessEqual(float(product['price']), 500)

    
    def test_product_filter_if_item_in_stock_only(self):
        response = self.client.get(self.product_url, {'in_stock': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for product in response.data['results']:
            self.assertGreater(product['stock'], 0)

    
    def test_search_products_by_name(self):
        response = self.client.get(self.product_url, {'search': 'Lamp'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for product in response.data['results']:
            self.assertIn('Lamp', product['name'])


    def test_search_products_by_slug(self):
        response = self.client.get(self.product_url, {'search': 'lamp'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for product in response.data['results']:
            self.assertIn('lamp', product['slug'])


    def test_order_by_price_descending(self):
        response = self.client.get(self.product_url, {'ordering': '-price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [product['price'] for product in response.data['results']]
        self.assertEqual(prices, sorted(prices, reverse=True))

    
    def test_order_by_price_ascending(self):
        response = self.client.get(self.product_url, {'ordering': 'price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [product['price'] for product in response.data['results']]
        self.assertEqual(prices, sorted(prices))
