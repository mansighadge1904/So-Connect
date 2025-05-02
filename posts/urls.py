from django.urls import path
from .views import create_post, create_story, dashboard, like_post, add_comment, mark_as_viewed, posts_by_hobby, explore, delete_comment, delete_post
from users.views import profile_view 


urlpatterns = [
    path("create/", create_post, name="create_post"),
    path("dashboard/", dashboard, name="dashboard"),
    path('stories/create/', create_story, name='create_story'),
    path('mark_as_viewed/<int:story_id>/', mark_as_viewed, name='mark_as_viewed'),
    path('profile/<str:username>', profile_view, name='profile'),
    path('like-post/<int:post_id>/', like_post, name='like-post'),
     path('delete/<int:post_id>/', delete_post, name='delete_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('hobby/<int:hobby_id>/', posts_by_hobby, name='posts_by_hobby'),
    path('explore/', explore, name='explore'),
]
