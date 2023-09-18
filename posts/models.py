from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from accounts.models import Profile
from django.utils import timezone
from django.utils.text import slugify
import datetime
from category.models import Category, SubCategory, Topic, Tag


class PostQueryset(models.QuerySet):
    def is_popular(self, views_limit):
        return self.filter(views__gte=views_limit)

    def is_recent(self):
        return self.filter(createdAt__lte=timezone.now())


class PostManger(models.Manager):
    def get_queryset(self):
        return PostQueryset(self.model, using=self._db)

    def is_popular(self, view_limit=50):
        return self.get_queryset().is_popular(view_limit)

    def is_recent(self):
        return self.get_queryset().is_recent()


class Post(models.Model):
    writer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="post_author",
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="topic_posts",
    )
    title = models.CharField(max_length=100)
    is_editors_choice = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="post_tags", blank=True)
    content = RichTextField(config_name="default")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    summary = models.TextField(
        max_length=300, blank=True, null=True, help_text="summary of the blog post"
    )
    image = models.ImageField(upload_to="posts/")
    views = models.IntegerField(default=1)
    bg_image = models.ImageField(upload_to="bg_posts/", blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    objects = PostManger()

    @property
    def comments(self):
        return self.get_comments().count()

    def __str__(self):
        return self.title
    
    class Meta:
        get_latest_by = "createdAt"

    def category(self):
        return self.topic.sub_category.category.name
    
    def get_sliders(self):
        return self.post_post_image.all().order_by("-id")[:10]
    
    def get_photos_count(self):
        return self.post_post_image.all()
    
    def get_absolute_url(self, **kwargs):
        return reverse("posts:post_detail", kwargs={"pk": self.pk, "slug": self.slug})

    def get_dashboard_absolute_url(self, **kwargs):
        return reverse(
            "dashboard:post_detail", kwargs={"pk": self.pk, "slug": self.slug}
        )

    def get_comment_upload_url(self, **kwargs):
        return reverse(
            "posts:upload_comment", kwargs={"pk": self.pk, "slug": self.slug}
        )

    def get_comments(self):
        return self.post_comments.all()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_post_image"
    )
    slider = models.ImageField(upload_to="images/slider/")

    def __str__(self):
        return f"Image id {self.pk}"


class PostComment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=100)
    comment = models.TextField()
    postedAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment Id: {self.pk}"

    def get_comment_reply(self):
        return self.comment_reply.all().order_by("-id").last()


class CommentReply(models.Model):
    comment = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name="comment_reply"
    )
    reply = models.TextField()

    def __str__(self):
        return f"comment reply to {self.comment.email}"
