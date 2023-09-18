from django.shortcuts import redirect, render, get_object_or_404
from .forms import SubscriptionForm
from dashboard.models import Subscription


def validate_user(request):
    if request.user.is_authenticated:
        return True
    return False


def post_subscription(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            if validate_user(request):
                if Subscription.objects.filter(
                    email=form.cleaned_data.get("email")
                ).exists():
                    return redirect("dashboard:posts")
                instance = form.save(commit=False)
                instance.profile = request.user.user_profile
                instance.save()
                form.save()
            return redirect("dashboard:auth:login")
        return redirect("dashboard:posts")
