from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from base.models import *
from user.models import *
from parler.models import TranslatableModel, TranslatedFields


class Classification(TranslatableModel):
    translations = TranslatedFields(    
        classification_name = models.CharField(_("Classification name"), max_length=50, blank=True, null=True),
    )
    
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.safe_translation_getter('user_type', any_language=True)
    
    class Meta:
        db_table = "classification"
        verbose_name = _("classification")
        verbose_name_plural = _("classifications")


class Storage(models.Model):    
    dimensions = models.CharField(_("Dimensions"), max_length=50, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=50, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    city = models.ForeignKey(City, verbose_name=_("City"), null=True, on_delete=models.SET_NULL)
    classification = models.ForeignKey(Classification, verbose_name=_("Classification"), null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(UserProfile, verbose_name=_("User"), null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = "storage"
        verbose_name = _("storage")
        verbose_name_plural = _("storages")
