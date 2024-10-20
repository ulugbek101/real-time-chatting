from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth import logout, get_user_model

from .forms import UserRegistrationForm

User = get_user_model()


class UserLoginView(LoginView):
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('chat')
    extra_context = {
        'title': 'Login'
    }



def user_registration(request):
    form = UserRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            password1, password2 = request.POST.get('password1'), request.POST.get('password2')

            if (password1 and password2) and len(password2) >= 8:
                user = form.save(commit=False)
                user.set_password(password2)
                user.save()
                # success message
                return redirect('login')
            else:
                ...
        else:
            ...

    context = {
        'form': form,
    }
    return render(request, 'app_users/registration.html', context)



def user_logout(request):
    logout(request)
    return redirect('login')
