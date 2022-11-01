# Generated by Django 4.1.1 on 2022-11-01 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0015_sharepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='RePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new', to=settings.AUTH_USER_MODEL)),
                ('original', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='original', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repost', to='post.post')),
            ],
        ),
    ]
