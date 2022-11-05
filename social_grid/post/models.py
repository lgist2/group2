from queue import Empty
from turtle import title
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    hashtags = models.CharField(max_length=50, blank=True,null=True)
    body = RichTextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='post_images/')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['date_created']
    def __str__(self):

        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{ self.account } - { self.post }.'
    
class SharePost(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_receiver')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_shared')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.sender.username} shared {self.post.title} to {self.receiver.username}'


class RePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='repost')
    original = models.ForeignKey(User, on_delete=models.CASCADE, related_name='original')
    new = models.ForeignKey(User, on_delete=models.CASCADE, related_name='new')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.new.username} reposted {self.post.title} from {self.original.username}'



    