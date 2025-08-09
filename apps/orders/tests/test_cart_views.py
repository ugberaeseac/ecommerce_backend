from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.products.models import Product, Category
from apps.orders.models import Cart, CartItem

User = get_user_model()


class CartViewTests(APITestCase):
    def setUp(self):
        # Users 
        self.user = User.objects.create_user(
            username="user_cart", email="user_cart@example.com", password="pass123"
        )
        self.other_user = User.objects.create_user(
            username="other_cart", email="other_cart@example.com", password="pass123"
        )
        self.admin = User.objects.create_superuser(
            username="admin_cart", email="admin_cart@example.com", password="adminpass"
        )

        # Category & Products 
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product1 = Product.objects.create(
            name="Product 1", price=Decimal("10.00"), stock=50, category=self.category
        )
        self.product2 = Product.objects.create(
            name="Product 2", price=Decimal("5.00"), stock=30, category=self.category
        )

        # Cart for self.user
        self.cart = Cart.objects.create(user=self.user)

        
        self.cart_item_list_url = reverse("cart_item-list")       
        self.cart_checkout_url = reverse("cart-checkout")   
        self.cart_detail_url = reverse("cart-detail", kwargs={"cart_id": self.cart.cart_id})

   
    def authenticate(self, user):
        self.client.force_authenticate(user=user)

      
    def test_add_item_to_cart(self):
        self.authenticate(self.user)
        payload = {
            "product": str(self.product1.product_id),
            "quantity": 2
        }
        res = self.client.post(self.cart_item_list_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 2)

  
    def test_cannot_add_item_with_zero_quantity(self):
        self.authenticate(self.user)
        payload = {
            "product": str(self.product1.product_id),
            "quantity": 0
        }
        res = self.client.post(self.cart_item_list_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_can_view_own_cart(self):
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        self.authenticate(self.user)
        res = self.client.get(self.cart_detail_url, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # CartSerializer nests items -> check items length
        self.assertEqual(len(res.data.get("items", [])), 1)


    def test_user_cannot_view_other_users_cart(self):
        other_cart = Cart.objects.create(user=self.other_user)
        self.authenticate(self.user)
        url = reverse("cart-detail", kwargs={"cart_id": other_cart.cart_id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_cart_item_quantity(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        self.authenticate(self.user)
        url = reverse("cart_item-detail", kwargs={"item_id": item.item_id})
        res = self.client.patch(url, {"quantity": 5}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)


    def test_remove_cart_item(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        self.authenticate(self.user)
        url = reverse("cart_item-detail", kwargs={"item_id": item.item_id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(item_id=item.item_id).exists())


    def test_user_cannot_modify_other_users_cart_item(self):
        other_cart = Cart.objects.create(user=self.other_user)
        item = CartItem.objects.create(cart=other_cart, product=self.product1, quantity=1)
        self.authenticate(self.user)
        url = reverse("cart_item-detail", kwargs={"item_id": item.item_id})
        res = self.client.patch(url, {"quantity": 3}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_access_any_cart(self):
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.authenticate(self.admin)
        res = self.client.get(self.cart_detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_checkout_creates_order_and_clears_cart(self):
        # Put items in cart
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.authenticate(self.user)
        res = self.client.post(self.cart_checkout_url, {}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # After checkout, cart should be empty
        self.assertEqual(self.cart.items.count(), 0)
