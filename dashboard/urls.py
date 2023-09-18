from django.urls import path, include
from . import views
from .functions.posts import post_subscription
from .uploads import upload_avatar_profile_image

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardHomeView.as_view(), name="home"),
    path("auth/", include("dashboard.auth.urls", namespace="auth")),
    path("profile/", views.DashboardProfileView.as_view(), name="profile"),
    path("posts/", views.DashboardListPostView.as_view(), name="posts"),
    path(
        "posts/create/",
        views.DashboardPostReqularCreateView.as_view(),
        name="post_regular_create",
    ),
    path(
        "posts/<int:pk>/<str:slug>/",
        views.DashboardPostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "posts/<int:pk>/<str:slug>/upload/",
        views.upload_multiple_post_images,
        name="multiple_upload_images",
    ),
    path("subscribe/", post_subscription, name="subscribe_newsletter"),
    #     uploads
    path("uplaod/avata/", upload_avatar_profile_image, name="profile_avatar_upload"),
]
