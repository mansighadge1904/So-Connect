from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Story
from .forms import PostForm, StoryForm
from django.utils.timezone import now
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
            return redirect("profile", username=request.user.username)
        else:
            print("From errors", form.errors)
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})

@login_required
def dashboard(request):
    # Existing context
    stories = Story.objects.all()
    posts = Post.objects.all()

    # ChitChat logic: get threads where user is involved
    
    

    # Get the "other user" from each thread
    
        
    context = {
        'stories': stories,
        'posts': posts,
        
    }

    return render(request, 'dashboard.html', context)

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

# @login_required
# @csrf_exempt
# def like_post(request, post_id):
#     if request.method == 'POST':
#         post = Post.objects.get(id=post_id)
#         user = request.user
#         liked = False

#         if user in post.likes.all():
#             post.likes.remove(user)
#         else:
#             post.likes.add(user)
#             liked = True

#         return JsonResponse({'likes': post.likes.count(), 'liked': liked})
def like_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            user = request.user

            if user in post.likes.all():
                post.likes.remove(user)
                liked = False
            else:
                post.likes.add(user)
                liked = True

            return JsonResponse({'likes': post.likes.count(), 'liked': liked})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

