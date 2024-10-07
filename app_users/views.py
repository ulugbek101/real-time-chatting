from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout


class UserLogin(LoginView):
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('chat')
    extra_context = {
        'title': 'Login'
    }


def user_logout(request):
    logout(request)
    return redirect('login')