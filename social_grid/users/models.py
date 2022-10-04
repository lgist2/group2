from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from PIL import Image

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(default=now)
    profile_img = models.ImageField(default='profile_images/logo-only-nobg.png', upload_to='profile_images/')

    def __str__(self):
        return self.user