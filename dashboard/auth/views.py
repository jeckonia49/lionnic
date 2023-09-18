from django.views import generic
from .forms import AdminLoginForm
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout

class DashboardLoginView(generic.FormView):
    template_name = "dashboard/auth/login.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("dashboard:home")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(email=email, password=password)
        if user and user.is_staff:
            login(self.request, user)
            return super(DashboardLoginView, self).form_valid(form)
        if user is None:
            messages.error(self.request, "Invalid login credentials")
            return redirect("dashboard:auth:login")
        if not user.is_staff:
            messages.error(
                self.request,
                f"You're not allowed to access this page. Contact admin at {settings.HELPLINE} for assistance",
            )
        return redirect("dashboard:auth:login")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:home")
        return super(DashboardLoginView, self).get(request, *args, **kwargs)


class DashboardForgotPasswordView(generic.TemplateView):
    template_name = "dashboard/auth/forgotpass.html"


class DashboardLockScreenView(generic.TemplateView):
    template_name = "dashboard/auth/lock.html"


def logout_view(request):
    logout(request)
    return redirect("dashboard:auth:login")