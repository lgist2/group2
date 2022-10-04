from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Account
from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm
from django.contrib.auth.decorators import login_required
from post.models import AddPost


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
             #need to add message to html instead
            Account.objects.create( user=user,)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required()
def profile(request):
    not_exists = False
    active_account = AddPost()
    active_account.account = request.user
    current_posts = AddPost.objects.all()
    user_posts = AddPost.objects.filter(account=active_account.account)
    if current_posts.exists():
        for posts in current_posts:
            if user_posts == posts.account:
                return render(request, 'users/profile.html', {'user_posts' : user_posts, 'not_exists': not_exists})
            else:
                return render(request, 'users/profile.html', {'user_posts' : user_posts, 'not_exists': not_exists})
    else:
        not_exists = True
        return render(request, 'users/profile.html',{'user_posts' : user_posts, 'not_exists': not_exists})

@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)
        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AccountUpdateForm(instance=request.user.account)
    
    return render(request,'users/update_profile.html',{'u_form' : u_form, 'a_form' : a_form})



