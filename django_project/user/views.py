from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from . import models
from . import serializers
from .permissions import IsProfileOwner


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = models.UserType.objects.all()
    serializer_class = serializers.UserTypeSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]


class LicenceViewSet(viewsets.ModelViewSet):
    queryset = models.Licence.objects.all()
    serializer_class = serializers.LicenceSerializer


class InterestViewSet(viewsets.ModelViewSet):
    queryset = models.Interest.objects.all()
    serializer_class = serializers.InterestSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
