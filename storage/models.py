from django.db import models
from django.utils.translation import gettext as _

from base.models import City
from user.models import UserProfile


class Storage(models.Model):
    dimensions = models.CharField(_("Dimensions"), max_length=50, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=50, blank=True, null=True)
    classification = models.CharField(
        _("Classification"), max_length=50, blank=True, null=True
    )
    active = models.BooleanField(_("Active"), default=True, null=True)

    city = models.ForeignKey(
        City, verbose_name=_("City"), null=True, on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        UserProfile, verbose_name=_("User"), null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.city.name}, {self.dimensions}, {self.classification}"

    class Meta:
        db_table = "storage"
        verbose_name = _("storage")
        verbose_name_plural = _("storages")
