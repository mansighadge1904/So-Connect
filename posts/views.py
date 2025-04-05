from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Story
from .forms import PostForm, StoryForm
from users.models import User
from django.utils.timezone import now

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("profile", user_id=request.user.id)
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})

@login_required
def dashboard_view(request):
    user = request.user
    following_users = User.objects.filter(followers__follower=user) 
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at') | Post.objects.filter(user=user).order_by('-created_at')
    posts = posts.distinct()

    stories = Story.objects.filter(expires_at__gt=now()).order_by('-created_at')

    return render(request, 'dashboard.html', {'posts': posts, 'stories': stories})

@login_required
def create_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('dashboard')  # Redirect back to the dashboard
    else:
        form = StoryForm()
    return render(request, 'create_story.html', {'form': form})