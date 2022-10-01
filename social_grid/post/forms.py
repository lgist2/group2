from django import forms
from django.forms import ModelForm
from .models import AddPost

class AddPostForm(ModelForm):
    class Meta:
        model = AddPost
        fields = [
            'title',
            'hashtags',
            'body',
            'image',
        ]
