from django import forms
from .models import Post, Story

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['text', 'image', 'video']