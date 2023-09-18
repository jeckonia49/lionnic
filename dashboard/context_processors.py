from posts.models import Post


def get_dashboard_popular(request):
    return dict(dashboard_popular=Post.objects.is_popular().order_by("?")[:4])
