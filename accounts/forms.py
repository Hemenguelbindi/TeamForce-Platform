from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm

from accounts.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'info', 'avatar')
        widgets = {
            'info': forms.Textarea(),
        }


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
        
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'gender', 'birth_date', 'info', 'avatar')

        widgets = {
            'info': forms.Textarea(),
        }


class Enter_code(forms.Form):
    code = forms.CharField(max_length=6)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
