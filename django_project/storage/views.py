from rest_framework import viewsets
from . import models
from user.models import UserProfile
from . import serializers
from rest_framework.permissions import IsAuthenticated


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = models.Classification.objects.all()
    serializer_class = serializers.ClassificationSerializer


class StorageViewSet(viewsets.ModelViewSet):
    queryset = models.Storage.objects.all()
    serializer_class = serializers.StorageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=UserProfile.objects.get(user=user))

