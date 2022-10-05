from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            ]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username',
            'email',
            ]

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'bio',
            'image',
            'birthday',
        ]
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'New Profile picture: '
        self.fields['bio'].label = 'Bio: '