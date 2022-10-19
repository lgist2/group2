from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

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
            messages.success(request, 'Account created for ' + username)
            
             #need to add message to html instead
            Account.objects.create( user=user,) #creates a profile account for the new user
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
    post_cnt = AddPost.objects.filter(account=active_account.account).count
    if current_posts.exists():
        for posts in current_posts:
            if user_posts == posts.account:
                return render(request, 'users/profile.html', {'user_posts' : user_posts, 'not_exists': not_exists, 'post_cnt':post_cnt})
            else:
                return render(request, 'users/profile.html', {'user_posts' : user_posts, 'not_exists': not_exists, 'post_cnt':post_cnt})
    else:
        not_exists = True
        return render(request, 'users/profile.html',{'user_posts' : user_posts, 'not_exists': not_exists, 'post_cnt':post_cnt})

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


@login_required
def search_user(request):
    if request.method == 'POST':
        search = request.POST['search']
        users = User.objects.filter(username__contains=search)
        return render(request, 'users/search_user.html', {'search' : search, 'users' : users})
    else:
        return render(request, 'users/search_user.html', {})

@login_required
def u_profile(request, u_id):
    user = User.objects.get(pk=u_id)
    return render(request, 'users/u_profile.html', {'user' : user })





