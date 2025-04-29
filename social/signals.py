# social/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follow, Notification

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            notification_type=Notification.FOLLOW,
            recipient=instance.following,
            sender=instance.follower,
        )
