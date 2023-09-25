from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext as _

from user.models import UserProfile


class Vehicle(models.Model):
    vin = models.CharField(_("VIN"), max_length=11, blank=True, null=True)
    dimensions = models.CharField(_("Dimensions"), max_length=50, blank=True, null=True)
    transport_capacity_kg = models.IntegerField(
        _("Transport capacity (KG)"), blank=True, null=True
    )
    transport_capacity_l = models.IntegerField(
        _("Transport capacity (L)"), blank=True, null=True
    )
    vehicle_category = models.CharField(
        _("Category"), max_length=50, blank=True, null=True
    )
    vehicle_brand = models.CharField(
        _("Vehicle brand"), max_length=50, blank=True, null=True
    )
    vehicle_model: CharField = models.CharField(
        _("Vehicle model"), max_length=50, blank=True, null=True
    )
    fuel_type = models.CharField(_("Fuel type"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    user = models.ForeignKey(
        UserProfile, verbose_name=_("User"), null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.vehicle_brand} {self.vehicle_model}"

    class Meta:
        db_table = "vehicle"
        verbose_name = _("vehicle")
        verbose_name_plural = _("vehicles")
