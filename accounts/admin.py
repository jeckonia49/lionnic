from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import AccountUser, Profile, Social


def _make_staff(modelname, request, queryset):
    queryset.update(is_staff=True)
_make_staff.shortdescription="Make Staff"

def _unmake_staff(modelname, request, queryset):
    queryset.update(is_staff=True)
    
_unmake_staff.shortdescription="Remove Staff"

@admin.register(AccountUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = AccountUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    actions = (_make_staff, _unmake_staff)


def _make_public(modelname, request, queryset):
    queryset.update(is_public=True)


_make_public.short_description = "Make Profile Public"


class SocialInline(admin.StackedInline):
    model = Social
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "full_name", "username", "is_public"]
    actions = (_make_public,)
    inlines = (SocialInline,)
