from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.products.models import Category, Product
from apps.users.models import User
import uuid


class CategoryProductTests(APITestCase):
    def setUp(self):
        # Create users
        self.admin = User.objects.create_superuser(email='admin@test.com', password='adminpass', username='admin')
        self.user = User.objects.create_user(email='user@test.com', password='userpass', username='user')

        # Auth headers
        self.client.login(email='admin@test.com', password='adminpass')
        self.category_list_url = reverse('category-list')
        self.product_list_url = reverse('product-list')

        # Sample category
        self.category = Category.objects.create(name="Books", slug="books")

    def authenticate_as_admin(self):
        self.client.force_authenticate(user=self.admin)


    def authenticate_as_user(self):
        self.client.force_authenticate(user=self.user)


    def test_create_category_as_admin_with_slug(self):
        self.authenticate_as_admin()
        data = {"name": "Laptops", "slug": "laptops"}
        response = self.client.post(self.category_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_category_as_admin_without_slug(self):
        self.authenticate_as_admin()
        data = {"name": "Romance Novels"}
        response = self.client.post(self.category_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['slug'], 'romance-novels')
	

    def test_create_category_as_user_without_admin_status(self):
        self.authenticate_as_user()
        data = {"name": "Phones", "slug": "phones"}
        response = self.client.post(self.category_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_categories_public(self):
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_category_detail_by_slug(self):
        url = reverse('category-detail', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.category.slug)


    def test_update_category_as_admin(self):
        self.authenticate_as_admin()
        url = reverse('category-detail', kwargs={'slug': self.category.slug})
        response = self.client.patch(url, {"name": "Updated Books"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Books")
        self.assertEqual(response.data["slug"], "updated-books")



    def test_delete_category_as_admin(self):
        self.authenticate_as_admin()
        url = reverse('category-detail', kwargs={'slug': self.category.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_create_product_as_admin_with_slug(self):
        self.authenticate_as_admin()
        data = {
            "name": "HP Spectre",
            "slug": "hp-spectre",
            "description": "Powerful ultrabook",
            "price": "2999.99",
            "stock": 5,
            "category": str(self.category.category_id)
        }
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_product_as_admin_without_slug(self):
        self.authenticate_as_admin()
        data = {
            "name": "HP Elitebook",
            "description": "Powerful Elitebook",
            "price": "5450.00",
            "stock": 9,
            "category": str(self.category.category_id)
        }
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['slug'], 'hp-elitebook')


    def test_create_product_some_missing_fields(self):
        self.authenticate_as_admin()
        response = self.client.post(self.product_list_url, {
            "name": "No Price",
            "stock": 3,
            "category": str(self.category.category_id)
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_products_public(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_product_detail_by_slug(self):
        product = Product.objects.create(
            name="Kindle", slug="kindle", description="E-book reader",
            price=199.99, stock=10, category=self.category
        )
        url = reverse('product-detail', kwargs={'slug': product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], product.slug)


    def test_update_product_as_admin(self):
        self.authenticate_as_admin()
        product = Product.objects.create(
            name="MacBook", slug="macbook", description="Laptop",
            price=2500, stock=3, category=self.category
        )
        url = reverse('product-detail', kwargs={'slug': product.slug})
        response = self.client.patch(url, {"price": 1999.99})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data["price"]), 1999.99)


    def test_delete_product_as_admin(self):
        self.authenticate_as_admin()
        product = Product.objects.create(
            name="Dell XPS", slug="dell-xps", description="Laptop",
            price=2200, stock=4, category=self.category
        )
        url = reverse('product-detail', kwargs={'slug': product.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_list_products_by_category_slug(self):
        Product.objects.create(
            name="Product A", slug="product-a", description="A",
            price=123.45, stock=3, category=self.category
        )
        url = reverse('category-product-list', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


    def test_invalid_category_slug_returns_404(self):
        url = reverse('category-product-list', kwargs={'slug': 'non-existent'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
