from django.contrib import admin
from .models import Category, SubCategory, Topic, Tag


@admin.register(Topic)
class AdminTopic(admin.ModelAdmin):
    list_display = ["sub_category", "topic"]


class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 0
    fields = ["category", "name", "image", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ["name", "sub_categories"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    inlines = (SubCategoryInline,)


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ["name"]
