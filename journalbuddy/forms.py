from django import forms
from .models import Journal
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["content", "rate"]


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        
        fields = ["username", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
