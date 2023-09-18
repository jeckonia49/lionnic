from django import forms
from posts.models import PostComment


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ["full_name", "email", "comment"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "comment": forms.Textarea(attrs={"placeholder": "Your Comment"}),
        }
