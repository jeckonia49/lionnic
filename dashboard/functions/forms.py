from django import forms
from dashboard.models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        fields = ["email"]
        model = Subscription

        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter email"}
            )
        }
