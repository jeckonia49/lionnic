from django.contrib import admin
from .models import Contact

# Register your models here.


def mark_is_read(modelname, request, queryset):
    queryset.update(is_read=True)


mark_is_read.short_description = "Mark read"


@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ["full_name", "email", "message", "is_read"]
    actions = (mark_is_read,)
