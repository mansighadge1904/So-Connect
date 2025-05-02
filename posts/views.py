from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Story, Comment, StoryView
from users.models import Hobby, Profile
from .forms import PostForm, StoryForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
from django.utils.timezone import now
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Process the hobbies text input
            hobbies_text = form.cleaned_data.get('hobbies')
            if hobbies_text:
                # Split hobbies by commas, strip spaces, and create or get Hobby objects
                hobbies_list = [hobby.strip() for hobby in hobbies_text.split(',')]
                for hobby_name in hobbies_list:
                    hobby, created = Hobby.objects.get_or_create(name=hobby_name)
                    post.hobbies.add(hobby)  # Associate the hobby with the post
            
            post.save()  # Save the post with the associated hobbies

            return redirect("profile", username=request.user.username)
        else:
            print("Form errors:", form.errors)
    else:
        form = PostForm()

    return render(request, "create_post.html", {"form": form})

@login_required
def dashboard(request):
    # Only show unexpired stories
    stories = Story.objects.filter(expires_at__gt=now()).order_by('-created_at')

    # Get IDs of stories viewed by the current user
    viewed_ids = StoryView.objects.filter(user=request.user).values_list('story_id', flat=True)

    # Access hobbies through the user's profile
    user_hobbies = request.user.profile.hobbies.all()

    # Filter posts that are related to the user's hobbies
    posts = Post.objects.filter(
        Q(hobbies__in=user_hobbies) | Q(user=request.user)
    ).distinct()

    context = {
        'stories': stories,
        'viewed_ids': viewed_ids,
        'posts': posts,
    }
    return render(request, 'dashboard.html', context)

@csrf_exempt  # (temporary only, better to handle CSRF properly later)
def mark_as_viewed(request, story_id):
    if request.method == 'POST':
        try:
            story = get_object_or_404(Story, id=story_id)
            print(f"Story found: {story.id}")  # debug print
            
            # you can mark as viewed here (optional for now)

            return JsonResponse({'success': True})
        except Exception as e:
            print("Error in view:", str(e))
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        print("Request method not POST, it was:", request.method)
        return JsonResponse({'success': False, 'message': 'Invalid method'})
    
def story_detail(request, id):
    # Fetch the story by ID, or return a 404 if not found
    story = get_object_or_404(Story, id=id)

    # Return the story detail to be rendered inside the modal
    return render(request, 'story_detail.html', {'story': story})  
      
@login_required
def create_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.expires_at = timezone.now() + timedelta(hours=24)
            story.save()
            return redirect('dashboard')  # Redirect back to the dashboard
    else:
        form = StoryForm()
    return render(request, 'create_story.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': post.likes.count()
    })
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_count = post.likes.count()  # This will give the number of likes
    comment_count = post.comments.count()  # Assuming you have a comments field/model
    return render(request, 'post/post_detail.html', {
        'post': post,
        'like_count': like_count,
        'comment_count': comment_count
    })
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        messages.error(request, "You are not allowed to delete this comment.")
        return redirect('dashboard')  # or the page you want to go back to

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def posts_by_hobby(request, hobby_id):
    hobby = Hobby.objects.get(id=hobby_id)
    posts = Post.objects.filter(hobbies=hobby)
    return render(request, 'posts_by_hobby.html', {'hobby': hobby, 'posts': posts})

def explore(request):
    # Get all posts and users without any filtering
    posts = Post.objects.exclude(user=request.user)
    users = Profile.objects.all()

    context = {
        'posts': posts,
        'users': users,
    }

    return render(request, 'explore.html', context)