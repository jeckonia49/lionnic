from django.contrib import admin
from posts.forms.admin import PostAdminForm

# Register your models here.
from posts.models import Post, PostComment, PostImage, CommentReply


def _approve_post(modelname, request, queryset):
    queryset.update(is_approved=True)


_approve_post.short_description = "Approve Post"


def _unapprove_post(modelname, request, queryset):
    queryset.update(is_approved=True)


_unapprove_post.short_description = "Unapprove Post"


class PostImageInline(admin.StackedInline):
    model = PostImage
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        "writer",
        "topic",
        "title",
        "createdAt",
        "updatedAt",
        "views",
        "is_approved",
        "comments",
    ]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["writer", "topic", "tags", "is_approved"]
    search_field = ["topic", "title", "tags"]
    list_per_page = 20
    inlines = (PostImageInline,)
    actions = (_approve_post, _unapprove_post)


@admin.register(PostComment)
class PostComment(admin.ModelAdmin):
    list_display = ["post", "email", "full_name", "postedAt"]


@admin.register(CommentReply)
class AdminReply(admin.ModelAdmin):
    pass
