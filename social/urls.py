from django.urls import path
from .views import follow_user, unfollow_user, like_post

urlpatterns = [
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('like/<int:post_id>/', like_post, name='like_post'),
]
