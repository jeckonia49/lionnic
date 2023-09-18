from django.db import models
from accounts.models import Profile

# Create your models here.


class Subscription(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="writer_subscription"
    )
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.email
