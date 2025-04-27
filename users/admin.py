from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, CustomUser

@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]

    # If you’ve added custom fields like "hobbies", include them:
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("hobbies",)}),  
    )

admin.site.register(Profile)
