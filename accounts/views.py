from django.shortcuts import render, redirect
from django.views import generic
from accounts.auth.forms import (
    LoginForm,
)
from .models import AccountUser
from django.contrib.auth import authenticate, login, logout


class AccountDashBoardView(generic.TemplateView):
    template_name = "accounts/dashboard/index.html"


class LoginView(generic.TemplateView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("assignments:home")
        return render(
            request, self.template_name, self.get_context_data(*args, **kwargs)
        )

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(*args, **kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        context = {}
        try:
            user = AccountUser.objects.filter(email=email).first()
            if user:
                obj = user.check_password(password)
                if obj:
                    login(request, user)
                    return redirect("dashboard:home")

        except AccountUser.DoesNotExist:
            context["InvalidCredentials"] = "Invalid Email Address"
            print(request.POST, user)
            context["error"] = "Invalid Credentials"
            return render(request, self.template_name, context)


class RegisterView(generic.TemplateView):
    template_name = "accounts/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("assignments:home")

        return render(
            request, self.template_name, self.get_context_data(*args, **kwargs)
        )

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        user = AccountUser.objects.create_user(
            email=email, password=password1, username=username
        )
        # print(user)
        return redirect("accounts:login")


def get_user_url(request, pk):
    user = AccountUser.objects.get(pk=pk)
    return render(request, "test.html", {"user": user})
