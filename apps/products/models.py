from django.db import models

from core.models import Timestamp
import uuid


class Category(Timestamp):
    """

    """
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    slug = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name



class Product(Timestamp):
    """
    """
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    stock = models.PositiveIntegerField(default=0, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
    
    @property
    def in_stock(self):
        return self.stock > 0

