from typing import Any
from django import http
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import is_valid_path
from django.views import generic
from posts.models import Post
from category.models import Tag
from .utils import get_next_or_prev
from django.http import JsonResponse
from posts.forms.forms import PostCommentForm
from paginator.paginators import Paginator
from django.http import HttpResponseRedirect

# import the mailer helper function from handler
from handlers.mailer import TemplateEmail


class HomeView(generic.TemplateView):
    template_name = "index.html"
    # queryset = Post
    # context
    
    def get_hero_display_posts(self, **kwargs):
        context = {
            "slider_posts": Post.objects.filter(is_approved=True)
            .all()
            .order_by("-createdAt"),
            "top_hero": Post.objects.filter(is_approved=True).all().order_by("?")[:1],
            "bottom": Post.objects.filter(is_approved=True).all().order_by("?")[:2],
            "top_posts": Post.objects.filter(topic__is_top_story=True).all()[:10],
            "best_category": Post.objects.is_popular(view_limit=100)
            .all()
            .order_by("?")
            .first(),
        }

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slider"] = self.get_hero_display_posts()["slider_posts"]
        context["top_hero_grid"] = self.get_hero_display_posts()["top_hero"]
        context["bottom_hero_grid"] = self.get_hero_display_posts()["bottom"]
        context["top_story"] = self.get_hero_display_posts()["top_posts"]
        # context['popular'] = Post.objects.is_popular().order_by("?")[:4]
        # context['recent'] = Post.objects.is_recent().order_by("?")[:4]
        # context['lim_tags'] = Tag.objects.all().order_by("?")[:10]
        context["best_post"] = Post.objects.filter(views__gte=100).first()
        context["best_posts"] = (
            Post.objects.is_popular(view_limit=50).order_by("-createdAt").all()
        )
        context["trending"] = (
            Post.objects.is_popular(view_limit=500).all().order_by("?")
        )
        return context

    def get(self, request, *args: Any, **kwargs: Any):

        # This is the implementation
        
        # mailer = TemplateEmail(
        #     "kwasa@gmail.com",
        #     "Testing email",
        #     "test",
        #     context={
        #   "user": request.user,
        #   "domain": get_current_site(request).domain,
        # }
        # )
        # mailer.send()

        return super().get(request, *args, **kwargs)

class PostListView(Paginator, generic.TemplateView):
    template_name = "pages/posts.html"
    queryset = Post
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        return context


class PostDetailView(generic.TemplateView):
    template_name = "pages/post.html"
    context_object_name = "post"
    queryset = Post

    def get_object(self, **kwargs):
        return get_object_or_404(
            self.queryset, pk=kwargs.get("pk"), slug=kwargs.get("slug")
        )

    def next_item_in_posts(self, **kwargs):
        next = get_next_or_prev(
            self.queryset.objects.all().order_by("pk"),
            self.get_object(**kwargs),
            "next",
        )
        return next

    def prev_item_in_posts(self, **kwargs):
        prev = get_next_or_prev(
            self.queryset.objects.all().order_by("pk"),
            self.get_object(**kwargs),
            "prev",
        )
        return prev

    def related_posts(self, **kwargs):
        return (
            self.queryset.objects.filter(
                topic__sub_category__name__exact=self.get_object(
                    **kwargs
                ).topic.sub_category.name
            )
            .all()
            .exclude(id=self.get_object(**kwargs).pk)
            .order_by("?")[:6]
        )

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["post"] = self.get_object(**kwargs)
        context["next"] = self.next_item_in_posts(**kwargs)
        context["prev"] = self.prev_item_in_posts(**kwargs)
        context["related"] = self.related_posts(**kwargs)
        context["comment_form"] = PostCommentForm()
        return context


# function views for posts request


def upload_comment(request, pk, slug, **kwargs):
    if request.method == "POST":
        form = PostCommentForm(request.POST)
        post = get_object_or_404(Post, pk=pk, slug=slug)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.save()
            form.save()
            return JsonResponse({"message": "Your Comment Was posted successfully"})
        return JsonResponse({"message": "Something went wrong"})



class LionnicFilterSearchView(Paginator, generic.TemplateView):
    template_name = "search.html"
    queryset = Post
    context_object_name = "posts"
    paginate_by = 100
    
    def get_search_params(self):
        return self.request.GET.get("lionnic_qs")
    
    def gq_queryset(self, **kwargs):
        return self.queryset.objects.filter(
            title__icontains=self.get_search_params(),
            is_approved=True).all().order_by("-id")
    
    def get_context_data(self, **kwargs):
        context = super(LionnicFilterSearchView, self).get_context_data(**kwargs)
        # context[self.context_object_name] = self.gq_queryset(**kwargs)
        return context
    
lionnicFilterView = LionnicFilterSearchView.as_view()

