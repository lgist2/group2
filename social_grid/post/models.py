from queue import Empty
from turtle import title
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.

class AddPost(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=15)
    hashtags = models.CharField(max_length=50, blank=True,null=True)
    body = RichTextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='post_images/')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    