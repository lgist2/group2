from django.contrib import admin
from .models import Post, Comment, SharePost, RePost

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SharePost)
admin.site.register(RePost)