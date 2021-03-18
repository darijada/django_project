from rest_framework import viewsets
from . import models
from user.models import UserProfile
from . import serializers
from rest_framework.permissions import IsAuthenticated


class CargoTypeViewSet(viewsets.ModelViewSet):
    queryset = models.CargoType.objects.all()
    serializer_class = serializers.CargoTypeSerializer


class TaskStatusViewSet(viewsets.ModelViewSet):
    queryset = models.TaskStatus.objects.all()
    serializer_class = serializers.TaskStatusSerializer


class TaskTypeViewSet(viewsets.ModelViewSet):
    queryset = models.TaskType.objects.all()
    serializer_class = serializers.TaskTypeSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=UserProfile.objects.get(user=user))
