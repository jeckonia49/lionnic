from django.urls import path, include
from . import views


app_name = "auth"

urlpatterns = [
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path(
        "forgot-password/",
        views.DashboardForgotPasswordView.as_view(),
        name="forgotpass",
    ),
    path("locked/", views.DashboardLockScreenView.as_view(), name="locked"),
    path("logout/", views.logout_view, name="logout"),
]
