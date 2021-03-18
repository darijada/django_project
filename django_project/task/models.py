from django.db import models
from django.utils.translation import gettext as _
from user.models import *
from vehicle.models import *
from parler.models import TranslatableModel, TranslatedFields


class CargoType(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "cargo_type"
        verbose_name = _("cargo_type")
        verbose_name_plural = _("cargo_types")


class TaskStatus(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "task_status"
        verbose_name = _("task_status")
        verbose_name_plural = _("task_statuses")


class TaskType(TranslatableModel):
    translations = TranslatedFields(    
        name = models.CharField(_("Name"), max_length=50, blank=True, null=True),
    )

    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "task_type"
        verbose_name = _("task_type")
        verbose_name_plural = _("task_types")


class Task(models.Model):  
    location_from = models.CharField(_("Location from"), max_length=50, blank=True, null=True)
    location_to = models.CharField(_("Location to"), max_length=50, blank=True, null=True)
    date_from = models.DateField(_("Date from"), blank=True, null=True)
    date_to = models.DateField(_("Date to"), blank=True, null=True)
    distance = models.DecimalField(_("Date to"), max_digits=5, decimal_places=2, blank=True, null=True)
    cargo_weight = models.IntegerField(_("Cargo weight"), blank=True, null=True)
    cargo_dimensions = models.CharField(_("Cargo dimensions"), max_length=50, blank=True, null=True)
    price = models.DecimalField(_("Price"), max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.CharField(_("Description"), max_length=1000, blank=True, null=True)
    rating = models.IntegerField(_("Rating"), blank=True, null=True)

    cargo_type = models.ForeignKey(CargoType, verbose_name=_("Cargo type"), null=True, on_delete=models.SET_NULL)
    task_status = models.ForeignKey(TaskStatus, verbose_name=_("Task status"), null=True, on_delete=models.SET_NULL)
    task_type = models.ForeignKey(TaskType, verbose_name=_("Task type"), null=True, on_delete=models.SET_NULL)
    submitter = models.ForeignKey(UserProfile, verbose_name=_("Submitter"), null=True, on_delete=models.SET_NULL)
    vehicle_category = models.ForeignKey(VehicleCategory, verbose_name=_("Vehicle category"), null=True, on_delete=models.SET_NULL)

    readonly_fields = ('submitter',)

    def __str__(self):
        return self.submitter + ', ' + self.task_type
    
    class Meta:
        db_table = "task"
        ordering = ["date_from"]
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
