from django.urls import path
from . import views

urlpatterns = [
    path('', views.chitchat_view, name='chitchat'),
    path('create-group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.chat_group_view, name='chat_group'),
    path('send/', views.send_message, name='send_message'),
    path('<str:username>/', views.chitchat_view, name='chat_with_user'),
    
]
