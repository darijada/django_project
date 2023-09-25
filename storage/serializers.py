from rest_framework import serializers

from . import models

from user.serializers import UserProfileSerializerShort


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Storage
        fields = "__all__"


class SuperUserStorageSerializer(serializers.ModelSerializer):
    user = UserProfileSerializerShort()

    class Meta:
        model = models.Storage
        fields = "__all__"
