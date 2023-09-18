from ckeditor.widgets import CKEditorWidget
from posts.models import Post
from django import forms


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = "__all__"
