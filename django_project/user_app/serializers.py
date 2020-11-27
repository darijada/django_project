from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User, UserProfile

class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        user = serializers.StringRelatedField(read_only=True)
        model = UserProfile
        fields = '__all__'