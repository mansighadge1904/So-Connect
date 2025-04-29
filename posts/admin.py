from django.contrib import admin
from .models import Post, Comment, Story

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Show 1 empty form for comments by default
    fields = ['user', 'content', 'created_at']  # Display these fields
    readonly_fields = ['created_at']  # Make created_at read-only
    
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'caption', 'created_at', 'likes_count']  # Ensure 'caption' is valid
    inlines = [CommentInline]  # Add the CommentInline to display comments within posts
    search_fields = ['user__username', 'caption']  # Add search functionality if necessary

    def likes_count(self, obj):
        return obj.likes.count()  # Display the count of likes
    likes_count.short_description = 'Likes'  # Optionally add a title for the column

class StoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'expires_at']
    # list_filter = ('created_at',)

# Register models with the Django admin
admin.site.register(Post, PostAdmin)  # Register Post with PostAdmin
admin.site.register(Story, StoryAdmin)  # Register Story with StoryAdmin
