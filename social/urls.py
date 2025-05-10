from django.urls import path, include
from .views import follow_user, unfollow_user, like_post, notifications, post_detail, my_followers, my_following

urlpatterns = [
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('notifications/', notifications, name='notifications'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('like_post/<int:post_id>/', include('posts.urls')),
    path('my-following/', my_following, name='my_following'),
    path('my-followers/', my_followers, name='my_followers'),
]
