from django import forms
from .models import Post, Story, Comment
from users.models import Hobby

class PostForm(forms.ModelForm):
    hobbies = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter hobbies separated by commas', 'rows': 4, 'class': 'form-control'}),
        required=False, 
        label="Enter hobbies"
    )

    class Meta:
        model = Post
        fields = ['caption', 'image', 'hobbies'] 

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['text', 'image', 'video']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']