from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Import UserAdmin
from django.contrib.auth.models import User
from social.models import Follow  # Import your Follow model

# Define functions to get followers and followings
def get_followers(user):
    return ", ".join([f.follower.username for f in Follow.objects.filter(following=user)])

def get_following(user):
    return ", ".join([f.following.username for f in Follow.objects.filter(follower=user)])

# Extend the UserAdmin to display followers and followings
class CustomUserAdmin(UserAdmin):  # Inherit from UserAdmin
    list_display = ('username', 'get_followers', 'get_following')

    def get_followers(self, obj):
        return get_followers(obj)
    get_followers.short_description = "Followers"

    def get_following(self, obj):
        return get_following(obj)
    get_following.short_description = "Following"

# Unregister default User and register the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# ✅ Register Follow Model to make it accessible in the admin panel
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
