from django.db import models
from django.utils.translation import gettext as _

from base.models import City
from storage.models import Storage
from user.models import UserProfile
from vehicle.models import Vehicle


class TaskStatus(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    code = models.CharField(_("Code"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "task_status"
        verbose_name = _("task_status")
        verbose_name_plural = _("task_statuses")


class TaskType(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    code = models.CharField(_("Code"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "task_type"
        verbose_name = _("task_type")
        verbose_name_plural = _("task_types")


class TransportationTask(models.Model):
    location_from = models.ForeignKey(
        City,
        verbose_name=_("Location from"),
        related_name="transport_location_from",
        null=True,
        on_delete=models.SET_NULL,
    )
    location_to = models.ForeignKey(
        City,
        verbose_name=_("Location to"),
        related_name="transport_location_to",
        null=True,
        on_delete=models.SET_NULL,
    )
    date_from = models.DateField(_("Date from"), blank=True, null=True)
    date_to = models.DateField(_("Date to"), blank=True, null=True)
    distance = models.DecimalField(
        _("Date to"), blank=True, null=True, decimal_places=2, max_digits=10
    )
    price = models.DecimalField(
        _("Price"), blank=True, null=True, decimal_places=2, max_digits=10
    )
    description = models.CharField(
        _("Description"), max_length=1000, blank=True, null=True
    )
    rating = models.IntegerField(_("Rating"), blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    cargo_type = models.CharField(_("Cargo Type"), max_length=50, blank=True, null=True)
    task_status = models.ForeignKey(
        TaskStatus, verbose_name=_("Task status"), null=True, on_delete=models.SET_NULL
    )
    task_type = models.ForeignKey(
        TaskType, verbose_name=_("Task type"), null=True, on_delete=models.SET_NULL
    )
    submitter = models.ForeignKey(
        UserProfile,
        verbose_name=_("Submitter"),
        related_name="transportation_task_submitter",
        null=True,
        on_delete=models.SET_NULL,
    )
    acceptor = models.ForeignKey(
        UserProfile,
        verbose_name=_("Acceptor"),
        related_name="transportation_task_acceptor",
        null=True,
        on_delete=models.SET_NULL,
    )
    vehicle = models.ForeignKey(
        Vehicle, verbose_name=_("Vehicle"), null=True, on_delete=models.SET_NULL
    )

    readonly_fields = (
        "submitter",
        "acceptor",
    )

    def __str__(self):
        return (
            f"{self.location_from.name} - {self.location_to.name}, {self.description}"
        )

    class Meta:
        db_table = "transportation_task"
        ordering = ["date_from"]
        verbose_name = _("transportation_task")
        verbose_name_plural = _("transportation_tasks")


class StorageTask(models.Model):
    date_from = models.DateField(_("Date from"), blank=True, null=True)
    date_to = models.DateField(_("Date to"), blank=True, null=True)
    price = models.DecimalField(
        _("Price"), blank=True, null=True, decimal_places=2, max_digits=10
    )
    description = models.CharField(
        _("Description"), max_length=1000, blank=True, null=True
    )
    rating = models.IntegerField(_("Rating"), blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    cargo_type = models.CharField(_("Cargo Type"), max_length=50, blank=True, null=True)
    task_status = models.ForeignKey(
        TaskStatus, verbose_name=_("Task status"), null=True, on_delete=models.SET_NULL
    )
    task_type = models.ForeignKey(
        TaskType, verbose_name=_("Task type"), null=True, on_delete=models.SET_NULL
    )
    submitter = models.ForeignKey(
        UserProfile,
        verbose_name=_("Submitter"),
        related_name="storage_task_submitter",
        null=True,
        on_delete=models.SET_NULL,
    )
    acceptor = models.ForeignKey(
        UserProfile,
        verbose_name=_("Acceptor"),
        related_name="storage_task_acceptor",
        null=True,
        on_delete=models.SET_NULL,
    )
    storage = models.ForeignKey(
        Storage, verbose_name=_("Storage"), null=True, on_delete=models.SET_NULL
    )

    readonly_fields = (
        "submitter",
        "acceptor",
    )

    def __str__(self):
        return f"{self.storage.name} - {self.description}"

    class Meta:
        db_table = "storage_task"
        ordering = ["date_from"]
        verbose_name = _("storage_task")
        verbose_name_plural = _("storage_tasks")


class ShippingTask(models.Model):
    location_from = models.ForeignKey(
        City,
        verbose_name=_("Location from"),
        related_name="shipping_location_from",
        null=True,
        on_delete=models.SET_NULL,
    )
    location_to = models.ForeignKey(
        City,
        verbose_name=_("Location to"),
        related_name="shipping_location_to",
        null=True,
        on_delete=models.SET_NULL,
    )
    date_from = models.DateField(_("Date from"), blank=True, null=True)
    date_to = models.DateField(_("Date to"), blank=True, null=True)
    distance = models.DecimalField(
        _("Date to"), blank=True, null=True, decimal_places=2, max_digits=10
    )
    cargo_weight = models.IntegerField(_("Cargo weight"), blank=True, null=True)
    cargo_dimensions = models.CharField(
        _("Cargo dimensions"), max_length=50, blank=True, null=True
    )
    price = models.DecimalField(
        _("Price"), blank=True, null=True, decimal_places=2, max_digits=10
    )
    description = models.CharField(
        _("Description"), max_length=1000, blank=True, null=True
    )
    rating = models.IntegerField(_("Rating"), blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    cargo_type = models.CharField(_("Cargo Type"), max_length=50, blank=True, null=True)
    task_status = models.ForeignKey(
        TaskStatus, verbose_name=_("Task status"), null=True, on_delete=models.SET_NULL
    )
    task_type = models.ForeignKey(
        TaskType, verbose_name=_("Task type"), null=True, on_delete=models.SET_NULL
    )
    submitter = models.ForeignKey(
        UserProfile,
        verbose_name=_("Submitter"),
        related_name="shipping_task_submitter",
        null=True,
        on_delete=models.SET_NULL,
    )
    acceptor = models.ForeignKey(
        UserProfile,
        verbose_name=_("Acceptor"),
        related_name="shipping_task_acceptor",
        null=True,
        on_delete=models.SET_NULL,
    )
    vehicle = models.ForeignKey(
        Vehicle, verbose_name=_("Vehicle"), null=True, on_delete=models.SET_NULL
    )

    readonly_fields = (
        "submitter",
        "acceptor",
    )

    def __str__(self):
        return (
            f"{self.location_from.name} - {self.location_to.name}, {self.description}"
        )

    class Meta:
        db_table = "shipping_task"
        ordering = ["date_from"]
        verbose_name = _("shipping_task")
        verbose_name_plural = _("shipping_tasks")
