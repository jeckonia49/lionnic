from django.shortcuts import redirect


def upload_avatar_profile_image(request):
    if request.method == "POST":
        profile = request.user.user_profile
        file = request.POST.get("avatar")
        profile.avatar = file
        profile.save()
        print("saved")
        return redirect(request.META.get("HTTP_REFERER", "posts:home"))
