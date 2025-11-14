from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'nickname', 'phone', 'gender', 'email', 'birth_date']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

