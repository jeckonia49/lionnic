from accounts.models import Profile


def get_profile(request):
    return dict(profile=Profile.objects.get(user=request.user))
