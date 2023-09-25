from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers

from user.models import UserProfile


class SeenUserNotificationsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = UserProfile.objects.get(user=self.request.user)
        notifications = models.Notification.objects.filter(
            user=user, seen=False, active=True
        )
        for notification in notifications:
            notification.seen = True
            notification.save()
        return notifications


class AllUserNotificationsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = UserProfile.objects.get(user=self.request.user)
        notifications = models.Notification.objects.filter(user=user, active=True)
        return notifications
