

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
    
    if request.user == followed_user:
        return JsonResponse({'success': False, 'message': "You cannot follow yourself!"})
    
    # Check if the user is already following
    follow_exists = Follow.objects.filter(follower=request.user, following=followed_user).exists()
    
    if not follow_exists:
        # Create follow record
        Follow.objects.create(follower=request.user, following=followed_user)

        # Create notification for the followed user
        notification = Notification.objects.create(
            recipient=followed_user,
            sender=request.user,
            notification_type='follow',
            post=None,
            is_read=False,
        )
        notification.save()

        # Get updated follower and following counts
        follower_count = followed_user.profile.followers.count()
        following_count = request.user.profile.following.count()

        return JsonResponse({
            'success': True, 
            'action': 'follow',
            'follower_count': follower_count,
            'following_count': following_count
        })
    else:
        # If already following, unfollow
        Follow.objects.filter(follower=request.user, following=followed_user).delete()

        # Get updated follower and following counts
        follower_count = followed_user.profile.followers.count()
        following_count = request.user.profile.following.count() 


        return JsonResponse({
            'success': True, 
            'action': 'unfollow',
            'follower_count': follower_count,
            'following_count': following_count
        })



@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()

    # Get updated follower and following counts
    follower_count = user_to_unfollow.profile.followers.count()
    following_count = request.user.profile.followers.count()

    return JsonResponse({
        'success': True,
        'action': 'unfollow',
        'follower_count': follower_count,
        'following_count': following_count
    })


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Check if user already likes the post
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

        # Create like notification
        notification = Notification.objects.create(
            recipient=post.author,  # The post owner receives the notification
            sender=user,            # The user who liked the post
            notification_type='like',
            post=post,              # The post being liked
            is_read=False,          # Initially unread
        )
        notification.save()

    return JsonResponse({'liked': liked})

@login_required
def comment_on_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    comment = request.POST.get('comment')  # assuming comment text is in the POST data

    # Create comment on the post (this assumes you have a Comment model)
    post.comments.create(user=user, comment_text=comment)

    # Create comment notification
    notification = Notification.objects.create(
        recipient=post.author,  # The post author gets notified
        sender=user,            # The user who commented
        notification_type='comment',
        post=post,              # The post being commented on
        comment=comment,        # The comment text
        is_read=False,          # Initially unread
    )
    notification.save()

    return redirect('post_detail', post_id=post.id)

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

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Optionally, you can pass additional context like comments or likes here
    return render(request, 'post_detail.html', {'post': post})

@login_required
def my_following(request):
    following_users = Follow.objects.filter(follower=request.user).select_related('following')
    return render(request, 'my_following.html', {'following_users': following_users})


@login_required
def my_followers(request):
    follower_users = Follow.objects.filter(following=request.user).select_related('follower')
    return render(request, 'my_followers.html', {'follower_users': follower_users})
