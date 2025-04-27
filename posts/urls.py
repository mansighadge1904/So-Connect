from django.urls import path
from .views import create_post, create_story, dashboard, like_post
from users.views import profile_view 


urlpatterns = [
    path("create/", create_post, name="create_post"),
    path("dashboard/", dashboard, name="dashboard"),
    
    path('stories/create/', create_story, name='create_story'),
    path('profile/<str:username>', profile_view, name='profile'),
    path('like-post/<int:post_id>/', like_post, name='like-post'),

]
