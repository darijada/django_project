from rest_framework import serializers

from . import models

from user.serializers import UserProfileSerializerShort


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vehicle
        fields = "__all__"


class SuperUserVehicleSerializer(serializers.ModelSerializer):
    user = UserProfileSerializerShort()

    class Meta:
        model = models.Vehicle
        fields = "__all__"
