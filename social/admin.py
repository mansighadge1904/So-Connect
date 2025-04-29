from django.contrib import admin
from django.contrib.auth import get_user_model
from social.models import Follow, Notification
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# Unregister CustomUser model if it's already registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Define functions to get followers and followings
def get_followers(user):
    return ", ".join([f.follower.username for f in Follow.objects.filter(following=user)])

def get_following(user):
    return ", ".join([f.following.username for f in Follow.objects.filter(follower=user)])

# Extend the UserAdmin to display followers and followings
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'get_followers', 'get_following')

    def get_followers(self, obj):
        return get_followers(obj)
    get_followers.short_description = "Followers"

    def get_following(self, obj):
        return get_following(obj)
    get_following.short_description = "Following"

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)

# Register Follow Model to make it accessible in the admin panel
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')  

# Register Notification Model to make it accessible in the admin panel
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'sender', 'is_read', 'timestamp')
    list_filter = ('notification_type', 'is_read')

admin.site.register(Notification, NotificationAdmin)
