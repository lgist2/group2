# Generated by Django 4.1.1 on 2022-10-05 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_account_birthday_alter_account_profile_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='profile_img',
            new_name='image',
        ),
    ]
