from django.db import models
from django.utils.translation import gettext as _


class Currency(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    unit_label = models.CharField(_("Unit label"), max_length=5, blank=True, null=True)
    subunit_label = models.CharField(
        _("Subunit label"), max_length=5, blank=True, null=True
    )
    code = models.CharField(_("Code"), max_length=5, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "currency"
        verbose_name = _("currency")
        verbose_name_plural = _("currencies")


class Country(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    code = models.CharField(_("Code"), max_length=5, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)
    currency = models.ForeignKey(
        Currency, verbose_name=_("Currency"), null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "country"
        verbose_name = _("country")
        verbose_name_plural = _("countries")


class City(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    code = models.CharField(_("Code"), max_length=5, blank=True, null=True)
    zip_code = models.CharField(_("ZIP Code"), max_length=10, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)
    country = models.ForeignKey(
        Country, verbose_name=_("Country"), null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "city"
        verbose_name = _("city")
        verbose_name_plural = _("cities")


class Language(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    code = models.CharField(_("Code"), max_length=5, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "language"
        verbose_name = _("language")
        verbose_name_plural = _("languages")
