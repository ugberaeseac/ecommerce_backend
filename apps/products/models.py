from django.db import models
from core.models import Timestamp
from django.utils.text import slugify
import uuid


class Category(Timestamp):
    """

    """
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
    
    
    def save(self, *args, **kwargs):
        if not self.slug or slugify(self.name) != self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name



class Product(Timestamp):
    """
    """
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    stock = models.PositiveIntegerField(null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=False)
    #image = models.ImageField(upload_to='products/', blank=True, null=False)

    class Meta:
        ordering = ['-created_at']
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    @property
    def in_stock(self) -> bool:
        return self.stock > 0

