from django.urls import path

from . import views

urlpatterns = [
    path('', views.no_room, name='no_room'),
]