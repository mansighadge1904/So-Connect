from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile  # Import Post here to avoid errors
from users import models  # Import models to avoid Hobby import issue

class SignupForm(UserCreationForm):
    hobbies = forms.ModelMultipleChoiceField(
        queryset=models.Hobby.objects.all(),  # Use models.Hobby to avoid ImportError
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'hobbies']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
            profile.hobbies.set(self.cleaned_data['hobbies'])  # Set hobbies
        return user

class LoginForm(AuthenticationForm):
    pass  # Using Django's default login form

class HobbyForm(forms.Form):
    hobbies = forms.ModelMultipleChoiceField(
        queryset=models.Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

