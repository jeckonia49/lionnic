from django import forms
from pages.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["full_name", "email", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "message": forms.Textarea(attrs={"placeholder": "Your message"}),
        }
