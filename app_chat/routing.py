from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat-room/<username>/", consumers.ChatRoomConsumer.as_asgi()),
]
