from django.db import models

# Create your models here.


class Subscriber(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "-timestamp"
    
    def __str__(self):
        return self.email
