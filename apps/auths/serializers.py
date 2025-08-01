from rest_framework import serializers
from apps.users.models import User


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=8, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
