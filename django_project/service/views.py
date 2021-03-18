from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from . import models
from . import serializers


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    permission_classes = [IsAuthenticated]