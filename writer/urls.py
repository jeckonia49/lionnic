from django.urls import path, include
from . import views

app_name = "writer"

urlpatterns = [
    path("<int:pk>/", views.WriterProfileView.as_view(), name="writer_view"),
]
