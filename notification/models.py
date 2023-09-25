from django.db import models
from django.utils.translation import gettext as _

from user.models import UserProfile
from task.models import TransportationTask, StorageTask, ShippingTask


class NotificationMessage(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    code = models.CharField(_("Code"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    class Meta:
        db_table = "notification_message"
        verbose_name = _("notification_message")
        verbose_name_plural = _("notification_messages")


class Notification(models.Model):
    seen = models.BooleanField(_("Seen"), default=False, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    notification_message = models.ForeignKey(
        NotificationMessage,
        verbose_name=_("Notification message"),
        null=True,
        on_delete=models.SET_NULL,
    )
    transportation_task = models.ForeignKey(
        TransportationTask,
        verbose_name=_("Transportation task"),
        null=True,
        on_delete=models.SET_NULL,
    )
    storage_task = models.ForeignKey(
        StorageTask,
        verbose_name=_("Storage task"),
        null=True,
        on_delete=models.SET_NULL,
    )
    shipping_task = models.ForeignKey(
        ShippingTask,
        verbose_name=_("Shipping task"),
        null=True,
        on_delete=models.SET_NULL,
    )
    user = models.ForeignKey(
        UserProfile, verbose_name=_("User"), null=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "user_notification"
        verbose_name = _("user_notification")
        verbose_name_plural = _("user_notifications")
