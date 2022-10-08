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
        
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['hashtags'].widget.attrs['class'] = 'form-control'
        self.fields['body'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'

