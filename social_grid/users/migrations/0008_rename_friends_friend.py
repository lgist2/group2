# Generated by Django 4.1.1 on 2022-10-21 05:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_friends'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Friends',
            new_name='Friend',
        ),
    ]
