from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from service.serializers import ServiceSerializer
from .models import UserType, User, UserProfile, Licence, Interest, Notification

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from config.mixins import TranslatedSerializerMixin


class UserTypeSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=UserType)

    class Meta:
        model = UserType
        fields = '__all__'


class LicenceSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Licence)

    class Meta:
        model = Licence
        fields = '__all__'


class InterestSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Interest)

    class Meta:
        model = Interest
        fields = '__all__'


class UserSerializer(UserCreateSerializer):
    user_type = UserTypeSerializer()
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    service = ServiceSerializer(many=True)
    licence = LicenceSerializer(many=True)
    interest = InterestSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = '__all__'


class NotificationSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    user = UserProfileSerializer(read_only=False)
    translations = TranslatedFieldsField(shared_model=Notification)

    class Meta:
        model = Notification
        fields = '__all__'