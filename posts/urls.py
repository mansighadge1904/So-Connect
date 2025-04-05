from django.urls import path
from .views import create_post, dashboard_view

urlpatterns = [
    path("create/", create_post, name="create_post"),
    path("dashboard/", dashboard_view, name="dashboard"),
]
