from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError('Users must have an email address.')
        
        kwargs.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        kwargs.setdefault('is_superuser', True)
        user = self.create_user(email, username=username, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email"), max_length=50, unique=True)
    username = models.CharField(_("username"), max_length=50, unique=True)
    is_active = models.BooleanField(_("active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=50, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, blank=True)
    address = models.CharField(_("address"), max_length=50, blank=True)
    city = models.CharField(_("city"), max_length=50, blank=True)
    county = models.CharField(_("county"), max_length=50, blank=True)
    country = models.CharField(_("city"), max_length=50, blank=True)
    phone_number = PhoneNumberField(_("phone number"), blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return "{} {}".format(last_name, first_name)
    
    class Meta:
        db_table = "user_profile"
        ordering = ["created_at"]
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")