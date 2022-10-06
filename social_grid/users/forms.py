from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    
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

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

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

    def __init__(self, *args,  **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'



class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'bio',
            'image',
            'birthday',
        ]
    def __init__(self, *args,  **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = 'New Profile picture: '
        self.fields['bio'].label = 'Bio: '
        self.fields['bio'].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        