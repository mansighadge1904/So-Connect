from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Profile, Hobby

User = get_user_model()

class UserModelTest(TestCase):
    
    def test_create_user(self):
        """Test creating a new user."""
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = User.objects.create_superuser(username='superuser', password='password123')
        self.assertEqual(superuser.username, 'superuser')
        self.assertTrue(superuser.check_password('password123'))
        self.assertTrue(superuser.is_superuser)

    def test_create_profile_for_new_user(self):
        """Test that a profile is created automatically when a user is created."""
        user = User.objects.create_user(username='testuser', password='password123')
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.image.name, 'default.jpg')  # Correct path

    def test_profile_str_method(self):
        """Test the __str__ method in the Profile model."""
        user = User.objects.create_user(username='testuser', password='password123')
        profile = Profile.objects.get(user=user)
        self.assertEqual(str(profile), 'testuser')

class HobbyModelTest(TestCase):

    def test_create_hobby(self):
        """Test creating a new hobby."""
        hobby = Hobby.objects.create(name='travelling', display_name='Roaming')
        self.assertEqual(hobby.name, 'travelling')
        self.assertEqual(hobby.display_name, 'Roaming')

    def test_hobby_str_method(self):
        """Test the __str__ method in the Hobby model."""
        hobby = Hobby.objects.create(name='travelling', display_name='Roaming')
        self.assertEqual(str(hobby), 'Roaming')

class ProfileHobbiesTest(TestCase):

    def test_add_hobby_to_profile(self):
        """Test adding hobbies to a profile."""
        user = User.objects.create_user(username='testuser', password='password123')
        hobby = Hobby.objects.create(name='travelling', display_name='Roaming')
        profile = Profile.objects.get(user=user)
        profile.hobbies.add(hobby)

        self.assertIn(hobby, profile.hobbies.all())

    def test_remove_hobby_from_profile(self):
        """Test removing hobbies from a profile."""
        user = User.objects.create_user(username='testuser', password='password123')
        hobby = Hobby.objects.create(name='travelling', display_name='Roaming')
        profile = Profile.objects.get(user=user)
        profile.hobbies.add(hobby)
        profile.hobbies.remove(hobby)

        self.assertNotIn(hobby, profile.hobbies.all())

class FollowFunctionalityTest(TestCase):

    def test_follow_user(self):
        """Test that a user can follow another user."""
        user1 = User.objects.create_user(username='user1', password='password123')
        user2 = User.objects.create_user(username='user2', password='password123')
        profile1 = Profile.objects.get(user=user1)
        profile2 = Profile.objects.get(user=user2)

        # User1 follows User2
        profile1.followers.add(profile2)
        
        self.assertIn(profile2, profile1.followers.all())
        self.assertIn(profile1, profile2.following.all())

    def test_unfollow_user(self):
        """Test that a user can unfollow another user."""
        user1 = User.objects.create_user(username='user1', password='password123')
        user2 = User.objects.create_user(username='user2', password='password123')
        profile1 = Profile.objects.get(user=user1)
        profile2 = Profile.objects.get(user=user2)

        # User1 follows User2 and then unfollows
        profile1.followers.add(profile2)
        profile1.followers.remove(profile2)
        
        self.assertNotIn(profile2, profile1.followers.all())
        self.assertNotIn(profile1, profile2.following.all())

class ProfileImageTest(TestCase):

    def test_profile_image_upload(self):
        """Test profile image upload functionality."""
        # Add image testing functionality here if needed (like using `django-storages` for storage)
        pass  # Placeholder for future image upload testing if required
