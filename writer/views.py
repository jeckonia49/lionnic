from django.shortcuts import get_object_or_404
from django.views import generic
from accounts.models import Profile
from posts.models import Post
from paginator.paginators import Paginator
from django.db.models import Sum


def post_view_count(request, field):
    return Post.objects.filter(writer=request).all().aggregate(total_views=Sum(field))


def post_object(queryset, **kwargs):
    return get_object_or_404(queryset, pk=kwargs.get("pk"), slug=kwargs.get("slug"))


class WriterProfileView(Paginator, generic.TemplateView):
    template_name = "writer/writer.html"
    queryset = Post
    paginate_by = 10
    context_object_name = "posts"

    def gq_queryset(self, **kwargs):
        return (
            self.queryset.objects.filter(writer=self.get_profile(**kwargs))
            .all()
            .order_by("-createdAt")
        )

    def get_context_data(self, **kwargs):
        context = super(WriterProfileView, self).get_context_data(**kwargs)
        context["profile"] = self.get_profile(**kwargs)
        context["total_views"] = post_view_count(self.get_profile(**kwargs), "views")
        print(context)
        return context

    def get_profile(self, **kwargs):
        return Profile.objects.filter(id=kwargs.get("pk")).first()
