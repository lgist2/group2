# Generated by Django 4.1.1 on 2022-10-26 16:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0010_addpost_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addpost',
            name='likes',
        ),
        migrations.AddField(
            model_name='addpost',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]