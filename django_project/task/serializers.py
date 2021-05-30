from rest_framework import serializers
from .models import *
from storage.serializers import StorageSerializer
from user.serializers import UserProfileSerializer
from vehicle.serializers import VehicleCategorySerializer, VehicleSerializer
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from config.mixins import TranslatedSerializerMixin


class CargoTypeSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=CargoType)
    class Meta:
        model = CargoType
        fields = '__all__'


class TaskStatusSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TaskStatus)
    class Meta:
        model = TaskStatus
        fields = '__all__'


class TaskTypeSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TaskType)

    class Meta:
        model = TaskType
        fields = '__all__'


class TransportationTaskSerializer(serializers.ModelSerializer):
    cargo_type = CargoTypeSerializer(many=False)
    task_status = TaskStatusSerializer(many=False)
    task_type = TaskTypeSerializer(many=False)
    submitter = UserProfileSerializer(read_only=True)
    acceptor = UserProfileSerializer(read_only=True)
    vehicle = VehicleSerializer(many=False)

    class Meta:
        model = TransportationTask
        fields = '__all__'


class StorageTaskSerializer(serializers.ModelSerializer):
    cargo_type = CargoTypeSerializer()
    task_status = TaskStatusSerializer()
    task_type = TaskTypeSerializer()
    submitter = UserProfileSerializer(read_only=True)
    acceptor = UserProfileSerializer(read_only=True)
    storage = StorageSerializer()

    class Meta:
        model = StorageTask
        fields = '__all__'


class ShippingTaskSerializer(serializers.ModelSerializer):
    cargo_type = CargoTypeSerializer()
    task_status = TaskStatusSerializer()
    task_type = TaskTypeSerializer()
    submitter = UserProfileSerializer(read_only=True)
    acceptor = UserProfileSerializer(read_only=True)
    vehicle_category = VehicleCategorySerializer()

    class Meta:
        model = ShippingTask
        fields = '__all__'

class TasksSerializer(serializers.Serializer):
    transportation_tasks = TransportationTaskSerializer(many=True)
    storage_tasks = StorageTaskSerializer(many=True)
    shipping_tasks = ShippingTaskSerializer(many=True)
