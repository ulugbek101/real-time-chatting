from django.urls import path

from . import views


urlpatterns = [
    path('', views.Chat.as_view(), name='chat'),
    path('chat/@<str:username>/', views.chat_room, name='chat_room'),
]
