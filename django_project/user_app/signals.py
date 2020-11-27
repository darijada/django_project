from django.dispatch import receiver
from djoser.signals import user_activated
from .models import User, UserProfile

@receiver(user_activated)
def create_user_profile(sender, user, request, **kwargs):
    UserProfile.objects.create(user=user)