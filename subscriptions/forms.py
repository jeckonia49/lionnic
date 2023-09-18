from django import forms
from .models import Subscriber


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email',]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "enteremail", "id": "subscribe-email", "placeholder": "example@gmail.com"})
        }
