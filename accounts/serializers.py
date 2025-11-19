from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # 회원가입에 필요한 모든 필드 포함
        fields = ['username', 'password', 'email', 'name', 'nickname', 'phone', 'gender', 'birth_date']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        # create_user 메서드로 비밀번호를 해시 처리
        return User.objects.create_user(**validated_data)


# JWT 로그인용 시리얼라이저
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data = super().validate(attrs)
        data.update({'username': user.username, 'email': user.email})
        return data
