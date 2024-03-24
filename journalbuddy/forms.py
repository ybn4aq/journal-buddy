from django import forms
from .models import Journal
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["date", "content", "rate", "media"]


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(forms.Form):
    usernmae = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
