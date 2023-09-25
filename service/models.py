from django.db import models
from django.utils.translation import gettext as _


class Service(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "service"
        verbose_name = _("service")
        verbose_name_plural = _("services")
