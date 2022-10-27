from datetime import datetime
from email.mime import image
from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from django.utils.timezone import now
from django.utils import timezone
from ckeditor.fields import RichTextField
from PIL import Image

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(default=now)
    bio = RichTextField(blank=True, null=True)
    image = models.ImageField(default='profile_images/logo-only-nobg.png', upload_to='profile_images/')
    posts_liked = models.ManyToManyField(Post, blank=True, related_name='posts_liked')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)



class FriendRequest(models.Model):
    #friend request consists of sender and reciever
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sender.username

    
