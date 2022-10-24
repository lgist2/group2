# Generated by Django 4.1.1 on 2022-10-24 16:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0014_account_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='folowings',
            field=models.ManyToManyField(blank=True, related_name='followings', to=settings.AUTH_USER_MODEL),
        ),
    ]
