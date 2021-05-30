from rest_framework import serializers
from user.serializers import UserProfileSerializer
from .models import VehicleBrand, VehicleModel, FuelType, VehicleCategory, Vehicle
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from config.mixins import TranslatedSerializerMixin


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = '__all__'


class VehicleModelSerializer(serializers.ModelSerializer):
    vehicle_brand = VehicleBrandSerializer()

    class Meta:
        model = VehicleModel
        fields = '__all__'


class FuelTypeSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=FuelType)

    class Meta:
        model = FuelType
        fields = '__all__'


class VehicleCategorySerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=VehicleCategory)

    class Meta:
        model = VehicleCategory
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_model = VehicleModelSerializer(many=False)
    fuel_type = FuelTypeSerializer(many=False)
    vehicle_category = VehicleCategorySerializer(many=False)
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Vehicle
        fields = '__all__'
