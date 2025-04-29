from django.urls import path
from .views import (
    signup_view,
    login_view,
    logout_view,
    profile_view,
    edit_profile,
    home_view,
    search_users_ajax,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('profile/<str:username>/', profile_view, name='profile'),  # REVERT THIS LINE
    path("profile/<str:username>/edit/", edit_profile, name="edit_profile"), # Keep username for edit
    path("", home_view, name="home"),
    path('search-users-ajax/', search_users_ajax, name='search_users_ajax'),
]
