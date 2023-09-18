from django.shortcuts import render


def handler404(request, excecption):
    return render(request, "handlers/404.html", {})


def handler500(request, *args, **kwargs):
    return render(request, "handlers/500.html", {})
