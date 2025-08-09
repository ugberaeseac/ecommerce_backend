from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem



class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.CharField(source='product.price', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


    class Meta:
        model = CartItem
        fields = ('product', 'product_name', 'price', 'quantity', 'total_price')



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ('cart_id', 'user', 'items')




class OrderItemSerializer(serializers.ModelSerializer):

    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'total_price')



class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'items', 'created_at', 'status')



class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)