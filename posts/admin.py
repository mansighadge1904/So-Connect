from django.contrib import admin
from .models import Post, Story

# Register your models here.
admin.site.register(Post)
@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at')
    list_filter = ('created_at',)