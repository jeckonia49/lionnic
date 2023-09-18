from django.urls import path
from . import views


app_name = "posts"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("posts/", views.PostListView.as_view(), name="posts"),
    path("search/", views.lionnicFilterView, name="search"),
    path("posts/<pk>/<slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path(
        "posts/<pk>/<slug>/upload-comment/", views.upload_comment, name="upload_comment"
    ),
]
