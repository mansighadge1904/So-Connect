from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile only if it doesn't already exist
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)
