from rest_framework import serializers

from . import models


class NotificationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationMessage
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    notification_message = NotificationMessageSerializer(read_only=True)

    class Meta:
        model = models.Notification
        fields = "__all__"
