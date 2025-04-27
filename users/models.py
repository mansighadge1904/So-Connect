from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import  AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class CustomUser(AbstractUser):
    hobbies = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


User= get_user_model()

class Hobby(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

def get_default_user():
    return User.objects.first().id if User.objects.exists() else None

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    hobbies = models.ManyToManyField(Hobby, related_name='profiles', blank=True)
    image = models.ImageField(upload_to="profile_pics/", default="default.jpg")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
