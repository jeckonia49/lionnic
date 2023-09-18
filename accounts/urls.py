from django.urls import path
from . import views

app_name = "accpounts"


urlpatterns = [
    path("", views.AccountDashBoardView.as_view(), name="dashboard"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    # path("<pk>/", views.get_user_url, name="user_detail"),
]
