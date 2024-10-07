from django.db.models.base import Model as Model
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class Chat(LoginRequiredMixin, ListView):
    template_name = 'app_chat/chat.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Chats list'
        return context


def chat_room(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'user': user,
        'title': f'Chat with @{user.username}'
    }
    return render(request, 'app_chat/chat_room.html', context)
