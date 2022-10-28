from django import forms
from django.forms import ModelForm
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'hashtags',
            'body',
            'image',
        ]
        
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['hashtags'].widget.attrs['class'] = 'form-control'
        self.fields['body'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'body',
        ]
        
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['class'] = 'form-control'