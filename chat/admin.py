from django.contrib import admin
from .models import ChatMessage, ChatGroup, GroupMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'message')

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at')
    filter_horizontal = ('members',)
    search_fields = ('name', 'creator__username')

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'sender', 'message', 'timestamp')
    search_fields = ('group__name', 'sender__username', 'message')
