

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Follow, Notification
from posts.models import Post
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def follow_user(request, user_id):
    followed_user = User.objects.get(id=user_id)
    
    # Prevent self-following
    if request.user == followed_user:
        messages.error(request, "You cannot follow yourself!")
        return redirect('profile', username=followed_user.username)

    if request.user != followed_user:
        # Check if the user is already following
        follow_exists = Follow.objects.filter(follower=request.user, followed=followed_user).exists()
        
        if not follow_exists:
            # Create follow record
            Follow.objects.create(follower=request.user, followed=followed_user)

            # Create notification for the followed user
            notification = Notification.objects.create(
                recipient=followed_user,  # The user being followed will receive the notification
                sender=request.user,       # The user who is following
                notification_type='follow',  # The type of notification (follow)
                post=None,                  # Optional: If there's a post associated
                comment=None,               # Optional: If there's a comment associated
                is_read=False,              # Notification is unread initially
            )
            notification.save()

        else:
            # If already following, unfollow
            Follow.objects.filter(follower=request.user, followed=followed_user).delete()
            # Optionally, delete or mark the notification as read when unfollowing

    return redirect('profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', user_id=user_id)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({'liked': liked})

@login_required
def notifications(request):
    # Get notifications for the logged-in user
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')

    # Mark all notifications as read
    if request.GET.get('mark_as_read'):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)

    return render(request, 'notifications.html', {
        'notifications': user_notifications
    })