from django import forms
from accounts.models import Profile


class AdminLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
