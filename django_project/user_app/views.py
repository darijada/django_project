
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from . import models
from . import serializers
from .permissions import IsOwnerProfileOrReadonly


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfileOrReadonly]

