from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="category/")

    class Meta:
        verbose_name = "Category"
        verbose_name = "Category"

    def __str__(self):
        return self.name

    @property
    def sub_categories(self):
        return self.get_sub_categories().count()

    def get_cat_topics(self):
        return self.sub_category.get_topics()
    
    def get_absolute_url(self):
        return reverse("category:category_detail", kwargs={
            "pk":self.pk,
            "slug": self.slug,
        })
    
    def get_sub_categories(self):
        return self.sub_category.all()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="sub_category"
    )
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="category/", blank=True, null=True)
    topics = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = "subcategory"
        verbose_name = "subcategory"

    def __str__(self):
        print(self.get_topics())
        return self.name

    @property
    def topics(self):
        return self.get_topics().count()

    def get_topics(self):
        return self.sub_category_topic.all()
    
    def save(self, *args, **kargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        return super(SubCategory, self).save(*args, **kargs)
    
    def get_absolute_url(self):
        return reverse(
            "category:sub_category_detail",
            kwargs={
                "category_slug": self.category.slug,
                "pk": self.pk,
                "sub_category_slug": self.slug,
            },
        )


class Topic(models.Model):
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="sub_category_topic"
    )
    topic = models.CharField(max_length=100)
    summary = models.TextField(
        max_length=300, help_text="Summary of what the topic is about"
    )
    is_top_story = models.BooleanField(default=False)
    
    def __str__(self):
        return self.topic

    def get_topic_posts(self):
        return self.topic_posts.all()


class TagQuerySet(models.QuerySet):
    def is_popular(self):
        return self.filter(tags__post_tags__gte=1)


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def is_popular(self):
        return self.get_queryset().is_popular()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    objects = TagManager()

    def __str__(self):
        return self.name
