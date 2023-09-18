from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from posts.models import PostImage
from .forms import UpdateProfileForm

# Create your views here.
from django.views import generic
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from accounts.models import Profile
from posts.models import Post
from paginator.paginators import Paginator
from .functions.forms import SubscriptionForm
from .forms import PostRegularForm


class CustomAuthorizerCheck(object):
    def _user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self._user().user_profile
        return context

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("dashboard:auth:login")
        return super(CustomAuthorizerCheck, self).get(*args, **kwargs)


class DashboardHomeView(CustomAuthorizerCheck, generic.TemplateView):
    template_name = "dashboard/index.html"
    posts = Post

    def _posts(self, limit=10):
        return (
            self.posts.objects.filter(writer=self._user().user_profile)
            .all()
            .order_by("-createdAt")[:limit]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_posts"] = self._posts()
        context["posts"] = self.posts.objects.filter(
            writer=self._user().user_profile
        ).all()
        return context


class DashboardProfileView(CustomAuthorizerCheck, generic.TemplateView):
    template_name = "dashboard/shared/pages/profile/index.html"
    queryset = Profile
    posts = Post
    profile_form = UpdateProfileForm

    def _writers(self):
        return (
            self.queryset.objects.filter(is_public=True)
            .exclude(user=self._user())
            .order_by("?")[:5]
        )

    """
    
    """

    def get_context_data(self, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context["writers"] = self._writers()
        context["pform"] = self.profile_form(
            initial={
                "user": profile.user,
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "avatar": profile.avatar,
                "bio": profile.bio,
            }
        )
        return context

    def post(self, *args, **kwargs):
        form = self.profile_form(
            self.request.POST,
            self.request.FILES,
            initial={"avatar": self.request.user.user_profile.avatar},
        )
        if form.is_valid():
            profile = Profile.objects.get(user=self.request.user)
            print(profile)
            profile.user = self.request.user
            profile.first_name = form.cleaned_data.get("first_name")
            profile.last_name = form.cleaned_data.get("last_name")
            profile.full_name = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            profile.avatar = form.cleaned_data.get("avatar")
            profile.save()
        return redirect("dashboard:profile")


class DashboardListPostView(CustomAuthorizerCheck, Paginator, generic.TemplateView):
    template_name = "dashboard/shared/pages/posts/list.html"
    queryset = Post
    context_object_name = "posts"
    paginate_by = 5
    subscription_form = SubscriptionForm
    
    def gq_queryset(self):
        return self.queryset.objects.filter(writer=self._user().user_profile).all().order_by("-id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_posts"] = self.queryset.objects.is_popular(
            view_limit=100
        ).order_by("-updatedAt")[:2]
        context["subscription_form"] = self.subscription_form()
        return context


class DashboardPostDetailView(CustomAuthorizerCheck, generic.TemplateView):
    template_name = "dashboard/shared/pages/posts/detail.html"
    queryset = Post

    def _post(self, **kwargs):
        return get_object_or_404(
            self.queryset, pk=kwargs.get("pk"), slug=kwargs.get("slug")
        )

    def get_context_data(self, **kwargs):
        context = super(DashboardPostDetailView, self).get_context_data(**kwargs)
        context["post"] = self._post(**kwargs)
        return context


class DashboardPostReqularCreateView(CustomAuthorizerCheck, generic.FormView):
    template_name = "dashboard/shared/pages/posts/creations/regular_post_create.html"
    form_class = PostRegularForm
    # success_url = reverse_lazy("")

    def get_success_url(self):
        return redirect("dashboard:posts")

    def get_context_data(self, **kwargs):
        context = super(DashboardPostReqularCreateView, self).get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def form_valid(self, form, **kwargs):
        instance = form.save(commit=False)
        instance.writer = self._user().user_profile
        instance.save()
        form.save()
        return redirect(instance.get_dashboard_absolute_url(**kwargs))

    def form_invalid(self, form):
        print(form.errors)
        return super(DashboardPostReqularCreateView, self).form_invalid(form)


def upload_multiple_post_images(request, **kwargs):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=kwargs.get("pk"), slug=kwargs.get("slug"))
        files = request.FILES.getlist("post_images")
        for fil in files:
            PostImage.objects.create(post=post, slider=fil)
        return redirect(post.get_dashboard_absolute_url(**kwargs))
