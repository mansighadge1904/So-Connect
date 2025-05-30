

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_GET
from .models import Hobby, Profile
from posts.models import Post, Story
from social.models import Follow
from .utils import normalize_hobbies 

from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

def get_default_user():
    return User.objects.get(username="admin")

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect to login page or dashboard
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request, username):
    user_profile_obj = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=user_profile_obj)
    posts = Post.objects.filter(user=user_profile_obj).order_by('-created_at')
    post_count = posts.count()
    follower_count = Follow.objects.filter(following=user_profile_obj).count()
    following_count = Follow.objects.filter(follower=user_profile_obj).count()
    stories = Story.objects.filter(user=user_profile_obj).order_by('-created_at')


    is_following = False
    if request.user.is_authenticated and request.user != user_profile_obj:
        is_following = Follow.objects.filter(follower=request.user, following=user_profile_obj).exists()

    # Fetch like and comment counts for each post
    posts_with_counts = []
    for post in posts:
        like_count = post.likes.count()
        comment_count = post.comments.count()
        posts_with_counts.append({'post': post, 'like_count': like_count, 'comment_count': comment_count})

    context = {
        'user_profile': profile,
        'user': user_profile_obj,
        'posts_with_counts': posts_with_counts, # Use this in the template
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_following': is_following,
        'is_own_profile': request.user == user_profile_obj,
        'user_profile_obj': user_profile_obj,
        'stories': stories,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        hobby_names = request.POST.get("hobbies", "")
        raw_hobby_list = [name.strip() for name in hobby_names.split(",") if name.strip()]

        # ✅ Normalize the hobbies using synonyms
        normalized_hobby_pairs = normalize_hobbies(raw_hobby_list)

        hobby_objects = []
        for normalized_name, display_name in normalized_hobby_pairs:
            hobby, created = Hobby.objects.get_or_create(
                name=normalized_name,
                defaults={"display_name": display_name}
            )
            # Update display_name if it's a new variation
            if hobby.display_name != display_name:
                hobby.display_name = display_name
                hobby.save()
            hobby_objects.append(hobby)

        profile.hobbies.set(hobby_objects)

        # ✅ Handle profile picture
        if "profile_picture" in request.FILES:
            profile.image = request.FILES["profile_picture"]

        user.save()
        profile.save()
        return redirect("profile", username=user.username)

    return render(request, "edit_profile.html", {
        "user": user,
        "profile": profile,
        "profile_hobbies": ", ".join([hobby.display_name for hobby in profile.hobbies.all()]),
    })


@require_GET
def search_users_ajax(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)  # Example query
    users_data = []

    for user in users:
        user_data = {
            'username': user.username,
            'profile_image_url': user.profile.image.url if user.profile.image else None,
        }
        users_data.append(user_data)

    return JsonResponse({'users': users_data})
