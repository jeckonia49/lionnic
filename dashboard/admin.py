from typing import Any
from django.contrib import admin
from .models import (
    Subscription,
)

# minor admin
from posts.models import (
        Post,
        PostImage,
        CommentReply,
        PostComment,
)

from category.models import (
    Category,
    SubCategory,
    Topic,
    Tag,
)
# Register your models here.


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["profile", "email"]


# create a new admin site separate from the main but simulate it in every aspect
class DashboardAdminSite(admin.AdminSite):
    site_header = "Dashboard Admin"
    site_title = "Dasboard Admin Portal"
    index_title = "Welcome to Newsfox"

# give it a name
dashboard_admin_site = DashboardAdminSite(name='DashboardAdmin')


class PostImageInline(admin.StackedInline):
    model = PostImage
    extra = 0

class PostAdmin(admin.ModelAdmin):
    
    # this method ensure that the admin can nly view his/her own posts
    # this is for secrity purposes but van be modified later as needed
    
    def get_queryset(self, request):
        return self.model.objects.filter(writer=request.user.user_profile).all()
    # ensure thath during the savin gof the model, the writer can save without having to 
    # select the writer whihc is the case in default django behavior

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if getattr(obj, "writer", None) is None:
            obj.writer = request.user.user_profile
        return super(PostAdmin, self).save_model(request, obj, form, change)
    
    list_display = ['title',"topic", "writer", "is_editors_choice", "views", "is_approved"]
    exclude = ("writer","is_approved", "is_editors_choice", "views")
    inlines = (PostImageInline, )
    prepopulated_fields = {"slug": ("title", )}
    list_filter = ["topic", "tags", "is_approved", "is_editors_choice"]
    search_field = ["topic", "title", "tags"]
    list_per_page = 20



# we could create this as an inline on the post admin class
# but we would not have the ability to restrcit the 
# writer from modifying the comment

class PostCommentAdmin(admin.ModelAdmin):
    list_display = ["post", "email", "full_name", "postedAt"]
    list_display_links = list_display

    # this method ensure that the writer cannot modify the comments
    # but he/she can only view
    def get_readonly_fields(self, request, obj):
        if obj:
            # return the available fields (only needed)
            return ["post", "email", "full_name", "comment"]
        return self.readonly_fields
    


dashboard_admin_site.register(Post, PostAdmin)
# dashboard_admin_site.register(PostImage)
# dashboard_admin_site.register(CommentReply)
dashboard_admin_site.register(PostComment, PostCommentAdmin)
# dashboard_admin_site.register(Category)
dashboard_admin_site.register(SubCategory)


# This class only allow the users to create the topic
# without setting the is_top_story
# whihc can only be done by the superadmin

class TopicAdmin(admin.ModelAdmin):
    list_display = ['sub_category', 'topic', 'is_top_story']
    exclude = ("is_top_story", )
    list_display_links = ('sub_category', 'topic', 'is_top_story')
    
    # prevent editing can only create
    # (same as the postcommentadmin method ==!)
    def get_readonly_fields(self, request, obj):
        if obj:
            return ['topic', 'sub_category','summary']
        return self.readonly_fields
    
    
dashboard_admin_site.register(Topic, TopicAdmin)


# dashboard_admin_site.register(Tag)

