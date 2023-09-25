from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from . import models


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "email",
            "is_active",
            "created_by_superuser",
            "created_at",
            "updated_at",
            "is_blocked",
            "is_deleted",
            "user_type",
        ]


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserType
        fields = "__all__"


class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Licence
        fields = "__all__"


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Interest
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = "__all__"


class UserProfileSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ("id", "name", "user")


class SuperuserUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = "email"
