from django import forms
from .models import Post, Story, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['text', 'image', 'video']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']