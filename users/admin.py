from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'get_hobbies', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

    # Include 'hobbies' from Profile in the fieldsets for admin form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile',)}),  # Add profile field here
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile',)}),  # Add profile field here
    )

    # Custom method to get hobbies from the Profile model
    def get_hobbies(self, obj):
        return ", ".join([hobby.name for hobby in obj.profile.hobbies.all()]) if obj.profile.hobbies.exists() else "No hobbies"
    get_hobbies.short_description = 'Hobbies'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)  # Make sure Profile is registered for the admin panel
