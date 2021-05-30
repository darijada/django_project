from rest_framework import serializers
from base.serializers import CitySerializer
from user.serializers import UserProfileSerializer
from .models import Storage, Classification
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from config.mixins import TranslatedSerializerMixin


class ClassificationSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Classification)

    class Meta:
        model = Classification
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False)
    classification = ClassificationSerializer()
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Storage
        fields = '__all__'