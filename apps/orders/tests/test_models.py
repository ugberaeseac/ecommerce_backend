from django.test import TestCase
from apps.users.models import User
from apps.products.models import Category, Product
from apps.orders.models import Order, OrderItem



class OrderModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@demo.com', username='testuser', password='password')

        self.category = Category.objects.create(name='Books')
        self.product_1 = Product.objects.create(
            name='African Literature',
            price=1500.00,
            stock=20,
            category=self.category
        )
        self.product_2 = Product.objects.create(
            name='Modern Farming Tools',
            price=5000.00,
            stock=10,
            category=self.category
        )


    def test_create_order_with_items(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.product_1, quantity=2)
        OrderItem.objects.create(order=order, product=self.product_2, quantity=1)

        self.assertEqual(order.products.count(), 2)
        self.assertEqual(order.orderitem_set.count(), 2)


    def test_order_item_total_price(self):
        order = Order.objects.create(user=self.user)
        item = OrderItem.objects.create(order=order, product=self.product_1, quantity=3)

        expected_total = 3 * self.product_1.price
        self.assertEqual(item.total_price, expected_total)


    def test_deleting_order_also_deletes_order_items(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.product_1, quantity=2)
        self.assertEqual(OrderItem.objects.count(), 1)

        order.delete()
        self.assertEqual(OrderItem.objects.count(), 0)


    def test_order_str_method(self):
        order = Order.objects.create(user=self.user)
        expected_str = f'Order {order.order_id} by {self.user.username} with email {self.user.email}'
        self.assertEqual(str(order), expected_str)


    def test_order_item_str_method(self):
        order = Order.objects.create(user=self.user)
        item = OrderItem.objects.create(order=order, product=self.product_1, quantity=1)
        expected_str = f'1x {self.product_1.name} in Order: {order.order_id}'
        self.assertEqual(str(item), expected_str)