from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name_mobile>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]