from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Hobby
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):
    hobbies = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your hobbies, separated by commas.'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'hobbies']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()  # Save the user first
            
            # The profile will be created automatically via the signal
            profile = Profile.objects.get(user=user)
            
            # Get hobbies entered by the user
            hobbies = self.cleaned_data.get('hobbies', '')
            
            # Split the hobbies string by commas, remove extra spaces, and add them
            hobby_list = [hobby.strip() for hobby in hobbies.split(',') if hobby.strip()]
            
            # Create or get each hobby and add to the profile
            for hobby_name in hobby_list:
                hobby, created = Hobby.objects.get_or_create(name=hobby_name)
                profile.hobbies.add(hobby)

        return user
