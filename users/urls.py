from django.urls import path
from .views import (
    signup_view,
    login_view,
    logout_view,
    profile_view,
    edit_profile,
    follow_user,
    unfollow_user,
    home_view,
    search_users_ajax,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('profile/<str:username>/', profile_view, name='profile'),  # REVERT THIS LINE
    path("profile/<str:username>/edit/", edit_profile, name="edit_profile"), # Keep username for edit
    path("follow/<str:username>/", follow_user, name="follow_user"),
    path("unfollow/<str:username>/", unfollow_user, name="unfollow_user"),
    path("", home_view, name="home"),
    path('search-users-ajax/', search_users_ajax, name='search_users_ajax'),
]