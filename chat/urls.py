from django.urls import path
from chat import views

urlpatterns = [
    path('inbox/', views.inbox, name="inbox"),
    
]
