from django.contrib import admin
from apps.users.models import User
from apps.products.models import Product
from apps.orders.models import Order, OrderItem


admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
