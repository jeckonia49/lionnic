from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from posts.models import Post
from django.views.generic import TemplateView
from sitemaps.views import site_sitemaps

# route to independent page
from dashboard.admin import dashboard_admin_site


urlpatterns = [
    path("about-us/", views.AboutUs.as_view(), name="about"),
    path("contact-us/", views.ContactUs.as_view(), name="contact"),
    path("privacy/", views.Privacy.as_view(), name="privacy"),
    path(
        "terms-and-condition/",
        views.TermsCondition.as_view(),
        name="terms-and-condition",
    ),
    path('lionnic-admin-login/', admin.site.urls),
    path("subscribe/", views.SubscriptionView.as_view(), name="subscribe-view"),
    # path("admin/", admin.site.urls),
    path("lionnic-dashbord-admin/", dashboard_admin_site.urls),
    path("", include("posts.urls", namespace="posts")),
    path("category/", include("category.urls", namespace="category")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("writer/", include("writer.urls", namespace="writer")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("sitemap.xml", sitemap, {"sitemaps": site_sitemaps}),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "handlers.views.handler404"
handler500 = "handlers.views.handler500"


admin.site.site_header = "Lionnic Margazone"
admin.site.site_title = "Lionnic Margazone Admin Site"
admin.site.index_title = "Lionnic Margazone Admin Site"
