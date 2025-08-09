from django.db import models
from core.models import Timestamp
from apps.users.models import User
from apps.products.models import Product
import uuid



class Order(Timestamp):
    """

    """
    class StatusChoice(models.TextChoices):
        PENDING = 'pending'
        CONFIRMED = 'confirmed'
        CANCELLED = 'cancelled'

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    status = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')


    def __str__(self):
        return f'Order {self.order_id} by {self.user.username} with email {self.user.email}'



class OrderItem(models.Model):
    """

    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()


    class Meta:
        unique_together = ('order', 'product')


    @property
    def total_price(self):
        return self.quantity * self.product.price
    
    
    def __str__(self):
        return f'{self.quantity}x {self.product.name} in Order: {self.order.order_id}'



class Cart(Timestamp):
    cart_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.user.username}\'s cart'



class CartItem(Timestamp):
    item_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


    class Meta:
        unique_together = ('cart', 'product')

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.quantity}x {self.product.name} in Cart: {self.cart.cart_id}'
