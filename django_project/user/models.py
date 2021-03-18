from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from base.models import *
from service.models import *
from parler.models import TranslatableModel, TranslatedFields


class UserManager(BaseUserManager):
    def create_user(self, user_type, email, password=None, **kwargs):
        """
        Creates and saves a User with the given user type, email and password.
        """
        if not user_type:
            raise ValueError('You need to choose user type.')
        if not email:
            raise ValueError('You need to enter email.')
        
        kwargs.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        user = self.model(user_type=user_type, email=email, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_type, email, password=None, **kwargs):
        """
        Creates and saves a Superuser with the given user type, email and password.
        """
        if not user_type:
            raise ValueError('You need to choose user type.')
        if not email:
            raise ValueError('You need to enter email.')

        kwargs.setdefault('is_superuser', True)
        email = self.normalize_email(email)
        user = self.model(user_type=user_type, email=email, **kwargs)

        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)        
        return user


class UserType(TranslatableModel): 
    translations = TranslatedFields(   
        user_type = models.CharField(_("User type"), max_length=50, blank=True, null=True)
    )

    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.user_type
    
    class Meta:
        db_table = "user_type"
        verbose_name = _("user_type")
        verbose_name_plural = _("user_types")


class Licence(TranslatableModel): 
    translations = TranslatedFields(   
        licence_name = models.CharField(_("Licence name"), max_length=50, blank=True, null=True)
    )

    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.licence_name
    
    class Meta:
        db_table = "licence"
        verbose_name = _("licence")
        verbose_name_plural = _("licences")


class Interest(TranslatableModel): 
    translations = TranslatedFields(   
        interest_name = models.CharField(_("Interest name"), max_length=50, blank=True, null=True)
    )

    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.interest_name
    
    class Meta:
        db_table = "interest"
        verbose_name = _("interest")
        verbose_name_plural = _("interests")


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), max_length=50, unique=True)
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    user_type = models.ForeignKey(UserType, verbose_name=_("User type"), null=True, on_delete=models.SET_NULL)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "user_account"
        ordering = ["created_at"]
        verbose_name = _("user_account")
        verbose_name_plural = _("user_accounts")


class UserProfile(models.Model):
   
    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    oib = models.CharField(_("OIB"), max_length=11, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=50, blank=True, null=True)
    contact_number = PhoneNumberField(_("Contact number"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, null=True)

    user = models.OneToOneField(User, verbose_name=_("User"), null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, verbose_name=_("City"), null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, verbose_name=_("Country"), null=True, on_delete=models.SET_NULL)
    language = models.ForeignKey(Language, verbose_name=_("Language"), null=True, on_delete=models.SET_NULL)
    service = models.ManyToManyField(Service, db_table="user_service")
    licence = models.ManyToManyField(Licence, db_table="user_licence")
    interest = models.ManyToManyField(Interest, db_table="user_interest")

    readonly_fields = ('user',)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "user_profile"
        ordering = ["created_at"]
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")


class Notification(TranslatableModel): 
    translations = TranslatedFields(   
        notification_text = models.CharField(_("Interest name"), max_length=50, blank=True, null=True)
    )

    user = models.OneToOneField(UserProfile, verbose_name=_("User"), null=True, on_delete=models.SET_NULL)
    read = models.BooleanField(_("Read"), default=True, null=True)
    active = models.BooleanField(_("Active"), default=True, null=True)

    def __str__(self):
        return self.notification_text
    
    class Meta:
        db_table = "notification"
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")