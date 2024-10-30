from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth import logout, get_user_model
from django.contrib import messages

from .forms import UserRegistrationForm, UserAuthenticationForm

User = get_user_model()


class UserLoginView(LoginView):
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('chat')
    extra_context = {
        'title': 'Login'
    }
    form_class = UserAuthenticationForm

    def get_success_url(self) -> str:
        messages.success(self.request, f'Welcome, {self.request.user.fullname} 👋')
        return super().get_success_url()

    def form_invalid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user_exists = get_user_model().objects.filter(email=email).exists()

        if not user_exists:
            messages.error(self.request, 'User was not found')
        elif user_exists and ('@' in email and not get_user_model().objects.get(email=email).check_password(password)):
            messages.error(self.request, 'Email or Password is incorrect')
        else:
            messages.error(self.request, 'Form filled incorrectly')

        return super().form_invalid(form)
    

def user_registration(request):
    form = UserRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            password1, password2 = request.POST.get('password1'), request.POST.get('password2')
            email = request.POST.get('email')

            if (password1 and password2) and len(password2) >= 8:
                user = form.save(commit=False)
                user.username = email[:email.index('@')]
                user.set_password(password2)
                user.save()
                messages.success(request, f'You have been successfully registered, now you can log in here 😀')
                return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'app_users/registration.html', context)



def user_logout(request):
    logout(request)
    return redirect('login')
