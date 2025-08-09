from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.products.models import Product, Category
from apps.orders.models import Cart, CartItem, Order, OrderItem

User = get_user_model()


class OrderViewTests(APITestCase):
    def setUp(self):
        # Users (username + email)
        self.user = User.objects.create_user(
            username="order_user", email="order_user@example.com", password="pass123"
        )
        self.other_user = User.objects.create_user(
            username="order_other", email="order_other@example.com", password="pass123"
        )
        self.admin = User.objects.create_superuser(
            username="order_admin", email="order_admin@example.com", password="adminpass"
        )

        # Category & Product
        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(
            name="African Literature", price=Decimal("150.00"), stock=20, category=self.category
        )

        # urls
        self.cart_checkout_url = reverse("cart-checkout")
        self.order_detail_name = "order-detail"
        self.order_status_name = "order-status"

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def create_order_from_cart(self, user):
        # ensure cart exists and has at least one item
        cart, _ = Cart.objects.get_or_create(user=user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)

        self.authenticate(user)
        res = self.client.post(self.cart_checkout_url, {}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, f"checkout failed: {res.data}")
        # get latest order for user
        order = Order.objects.filter(user=user).order_by("-created_at").first()
        self.assertIsNotNone(order)
        # ensure orderitems were created
        self.assertGreater(OrderItem.objects.filter(order=order).count(), 0)
        return order

    def test_user_can_create_order_from_cart(self):
        order = self.create_order_from_cart(self.user)
        self.assertEqual(order.user, self.user)

    def test_user_can_retrieve_own_order(self):
        order = self.create_order_from_cart(self.user)
        self.authenticate(self.user)
        url = reverse(self.order_detail_name, kwargs={"order_id": order.order_id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("order_id"), str(order.order_id))

    def test_user_cannot_access_other_users_order(self):
        order = self.create_order_from_cart(self.user)
        self.authenticate(self.other_user)
        url = reverse(self.order_detail_name, kwargs={"order_id": order.order_id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_any_order(self):
        order = self.create_order_from_cart(self.user)
        self.authenticate(self.admin)
        url = reverse(self.order_detail_name, kwargs={"order_id": order.order_id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_can_delete_own_order(self):
        order = self.create_order_from_cart(self.user)
        self.authenticate(self.user)
        url = reverse(self.order_detail_name, kwargs={"order_id": order.order_id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(order_id=order.order_id).exists())

    def test_admin_can_update_order_status(self):
        order = self.create_order_from_cart(self.user)
        self.authenticate(self.admin)
        url = reverse(self.order_status_name, kwargs={"order_id": order.order_id})
        res = self.client.patch(url, {"status": "confirmed"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "confirmed")
