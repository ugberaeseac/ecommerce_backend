from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.UUIDField(write_only=True)
    class Meta:
        model = Product
        fields = ('product_id', 'name', 'slug', 'description', 'price', 'category', 'stock', 'in_stock')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value


    def create(self, validated_data):
        category_id = validated_data.pop('category')
        category = Category.objects.get(category_id=category_id)
        product = Product.objects.create(category=category, **validated_data)
        return product


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('category_id', 'name', 'slug', 'products')


