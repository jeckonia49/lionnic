from category.models import Category, SubCategory, Topic, Tag
from posts.models import Post
from django.contrib.sites.shortcuts import get_current_site


def get_categories(request):
    return dict(
        nav_categories=Category.objects.all().order_by("-id")[:8],
        footer_categories=Category.objects.all().order_by("-id")[:6],
        editors_choice=Post.objects.filter(is_editors_choice=True).all().order_by("-createdAt")[:5],
        recents=Post.objects.is_recent().all().order_by("-createdAt")[:8],
        popular=Post.objects.is_popular().order_by("?")[:4],
        recent=Post.objects.is_recent().order_by("?")[:4],
        side_categories=Category.objects.all().order_by("-id")[:5],
        lim_tags=Tag.objects.all().order_by("?")[:10],
    )


def sites_context_data(request):
    if request.is_secure():
        protocol = "https"
    protocol = "http"
    return dict(
        site_domail=get_current_site(request).domain,
        protocol=protocol,
    )
