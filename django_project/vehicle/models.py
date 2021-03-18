from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from user.models import *

from parler.models import TranslatableModel, TranslatedFields

class VehicleBrand(models.Model):    
    brand_name = models.CharField(_("Brand name"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.brand_name
    
    class Meta:
        db_table = "vehicle_brand"
        verbose_name = _("vehicle brand")
        verbose_name_plural = _("vehicle brands")


class VehicleModel(models.Model):    
    model_name = models.CharField(_("Model name"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    vehicle_brand = models.ForeignKey(VehicleBrand, verbose_name=_("Vehicle brand"), null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.model_name
    
    class Meta:
        db_table = "vehicle_model"
        verbose_name = _("vehicle model")
        verbose_name_plural = _("vehicle models")


class FuelType(TranslatableModel):
    translations = TranslatedFields(    
        fuel_type_name = models.CharField(_("Fuel type"), max_length=50, blank=True, null=True),
    )

    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.fuel_type_name
    
    class Meta:
        db_table = "fuel_type"
        verbose_name = _("fuel type")
        verbose_name_plural = _("fuel types")


class VehicleCategory(TranslatableModel):
    translations = TranslatedFields(    
        category_name = models.CharField(_("Category name"), max_length=50, blank=True, null=True),
    )
    
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table = "vehicle_category"
        verbose_name = _("vehicle category")
        verbose_name_plural = _("vehicle categories")


class Vehicle(models.Model):    
    vin = models.CharField(_("VIN"), max_length=11, blank=True, null=True)
    dimensions = models.CharField(_("Dimensions"), max_length=50, blank=True, null=True)
    transport_capacity_kg = models.IntegerField(_("Transport capacity (KG)"), blank=True, null=True)
    transport_capacity_l = models.IntegerField(_("Transport capacity (L)"), blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    vehicle_model = models.ForeignKey(VehicleModel, verbose_name=_("Vehicle model"), null=True, on_delete=models.SET_NULL)
    fuel_type = models.ForeignKey(VehicleBrand, verbose_name=_("Fuel type"), null=True, on_delete=models.SET_NULL)
    vehicle_category = models.ForeignKey(VehicleCategory, verbose_name=_("Vehicle category"), null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(UserProfile, verbose_name=_("User"), null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.model_name
    
    class Meta:
        db_table = "vehicle"
        verbose_name = _("vehicle")
        verbose_name_plural = _("vehicles")