from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers

from user.models import UserProfile
from user.permissions import IsSuperUser


class SuperUserVehicleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Vehicle.objects.filter(active=True)
    serializer_class = serializers.SuperUserVehicleSerializer
    permission_classes = [IsSuperUser]


class UserVehicleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = models.Vehicle.objects.filter(
            user=UserProfile.objects.get(user=user), active=True
        )
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=UserProfile.objects.get(user=user))
