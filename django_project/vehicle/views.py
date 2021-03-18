from rest_framework import viewsets
from . import models
from user.models import UserProfile
from . import serializers
from rest_framework.permissions import IsAuthenticated


class VehicleBrandViewSet(viewsets.ModelViewSet):
    queryset = models.VehicleBrand.objects.all()
    serializer_class = serializers.VehicleBrandSerializer


class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = models.VehicleModel.objects.all()
    serializer_class = serializers.VehicleModelSerializer


class FuelTypeViewSet(viewsets.ModelViewSet):
    queryset = models.FuelType.objects.all()
    serializer_class = serializers.FuelTypeSerializer


class VehicleCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.VehicleCategory.objects.all()
    serializer_class = serializers.VehicleCategorySerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = models.Vehicle.objects.all()
    serializer_class = serializers.VehicleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=UserProfile.objects.get(user=user))
