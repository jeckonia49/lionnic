from django import forms
from posts.models import Post
from ckeditor.widgets import CKEditorWidget
from category.models import Topic, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "topic",
            "title",
            "is_editors_choice",
            "tags",
            "content",
            "summary",
            "image",
            "bg_image",
        ]
        widgets = {
            "content": CKEditorWidget(config_name="default"),
        }
