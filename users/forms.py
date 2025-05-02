from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Hobby
from django.contrib.auth import get_user_model
from .utils import normalize_hobbies

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

            # Ensure profile exists
            profile, created = Profile.objects.get_or_create(user=user)

            # Get hobbies entered by the user
            hobbies = self.cleaned_data.get('hobbies', '')

            # Split the hobbies string by commas, remove extra spaces, and add them
            hobby_list = [hobby.strip() for hobby in hobbies.split(',') if hobby.strip()]

            # Normalize the hobby names using synonyms (you could also include synonyms mapping here)
            normalized_hobby_pairs = normalize_hobbies(hobby_list)

            # Create or get each hobby and add it to the profile
            for normalized, display in normalized_hobby_pairs:
                hobby, created = Hobby.objects.get_or_create(name=normalized, defaults={"display_name": display})
                
                # Update the display_name if it's different from the default one
                if hobby.display_name != display:
                    hobby.display_name = display
                    hobby.save()

                profile.hobbies.add(hobby)

        return user
