# Generated by Django 4.1.1 on 2022-10-04 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='bday',
            new_name='birthday',
        ),
    ]
