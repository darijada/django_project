from rest_framework import serializers
from .models import Currency, Country, City, Language
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from config.mixins import TranslatedSerializerMixin


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class CountrySerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Country)
    currency = CurrencySerializer()

    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=City)
    country = CountrySerializer()

    class Meta:
        model = City
        fields = '__all__'

class LanguageSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Language)

    class Meta:
        model = Language
        fields = '__all__'