from django.shortcuts import render, get_object_or_404
from django.views import generic
from accounts.models import Profile
from django.shortcuts import redirect
from posts.models import Post
from django.db.models import Sum
from writer.forms.posts.forms import PostForm
from django.utils.text import slugify
from paginator.paginators import Paginator


def post_view_count(request, field):
    return Post.objects.filter(writer=request).all().aggregate(total_views=Sum(field))


def post_object(queryset, **kwargs):
    return get_object_or_404(queryset, pk=kwargs.get("pk"), slug=kwargs.get("slug"))
