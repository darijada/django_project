from rest_framework import serializers
from .models import *
from user.serializers import UserProfileSerializer
from vehicle.serializers import VehicleCategorySerializer
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from config.mixins import TranslatedSerializerMixin


class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = '__all__'


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'


class TaskTypeSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TaskType)

    class Meta:
        model = TaskType
        fields = '__all__'


class TaskSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Task)
    cargo_type = CargoTypeSerializer()
    task_status = TaskStatusSerializer()
    task_type = TaskTypeSerializer()
    submitter = UserProfileSerializer(read_only=True)
    vehicle_category = VehicleCategorySerializer()

    class Meta:
        model = Task
        fields = '__all__'

