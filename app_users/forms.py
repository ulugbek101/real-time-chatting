from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=100, widget=forms.PasswordInput(attrs={'type': 'password'}))
    password2 = forms.CharField(
        max_length=100, widget=forms.PasswordInput(attrs={'type': 'password'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'outline-none bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            })