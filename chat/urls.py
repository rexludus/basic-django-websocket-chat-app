from django.urls import path

from . import views

urlpatterns = [
    # root path /chat channel
    path('', views.index, name='index'),
    # chat room name -> route to the chat room name
    path('<str:room_name>/', views.room, name='room'),
]