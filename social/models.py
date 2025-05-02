from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from posts.models import Post

User = get_user_model()

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.following}"

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follows


   

# Now you can safely reference Post in Notification
class Notification(models.Model):
    # Notification Types
    FOLLOW = 'follow'
    UNFOLLOW = 'unfollow'
    LIKE = 'like'
    COMMENT = 'comment'

    NOTIFICATION_TYPES = [
        (FOLLOW, 'Follow'),
        (UNFOLLOW, 'Unfollow'),
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
    ]

    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES,
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        null=True,
        blank=True
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    content_object = GenericForeignKey('content_type', 'object_id')

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )

    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.notification_type in [self.LIKE, self.COMMENT] and not self.post:
            raise ValidationError(f"Post must be selected for '{self.notification_type}' notifications.")

    def __str__(self):
        return f"{self.sender} {self.notification_type} {self.content_object} to {self.recipient}"