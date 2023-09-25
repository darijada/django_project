from rest_framework import serializers

from . import models

from vehicle import serializers as vehicle_serializers
from storage import serializers as storage_serializers


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskStatus
        fields = "__all__"


class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskType
        fields = "__all__"


class TransportationTaskSerializer(serializers.ModelSerializer):
    vehicle = vehicle_serializers.VehicleSerializer()

    class Meta:
        model = models.TransportationTask
        fields = "__all__"


class StorageTaskSerializer(serializers.ModelSerializer):
    storage = storage_serializers.StorageSerializer()

    class Meta:
        model = models.StorageTask
        fields = "__all__"


class ShippingTaskSerializer(serializers.ModelSerializer):
    vehicle = vehicle_serializers.VehicleSerializer()

    class Meta:
        model = models.ShippingTask
        fields = "__all__"
