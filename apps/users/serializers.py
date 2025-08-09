from rest_framework import serializers
from apps.orders.serializers import OrderSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)

    class Meta:
        model = User
        #fields = '__all__'
        fields = (
        'user_id',
        'first_name',
        'last_name',
        'username',
        'password',
        'email',
        'phone_number',
        'orders',
        'is_superuser',
        'is_staff',
        'is_active',
        'created_at',
        'updated_at',
        )


