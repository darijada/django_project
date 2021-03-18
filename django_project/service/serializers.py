from rest_framework import serializers
from .models import Service

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from config.mixins import TranslatedSerializerMixin


class ServiceSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Service)

    class Meta:
        model = Service
        fields = '__all__'
