from asyncio.windows_events import NULL
from tkinter import E
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
import json

from .models import Account, FriendRequest
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
            #Relationship.objects.create(user=user,)
            Account.objects.create(user=user,) #creates a profile account for the new user
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
    friend_cnt = Account.objects.filter(friends=active_account.account).count
    friend_requests = FriendRequest.objects.filter(reciever=request.user)
    current_users = User.objects.exclude(username=request.user)
    #followers = Account.objects.filter(followers=active_account.account).count
    #followings = Account.objects.filter(followings=active_account.account).count
    if current_posts.exists():
        for posts in current_posts:
            if user_posts == posts.account:
                return render(request, 'users/profile.html', {'user_posts' : user_posts, 
                'not_exists': not_exists, 
                'post_cnt':post_cnt,
                'friend_requests' : friend_requests,
                'current_users' : current_users,
                'friend_cnt' : friend_cnt,
                })
            else:
                return render(request, 'users/profile.html', {'user_posts' : user_posts,
                'not_exists': not_exists, 
                'post_cnt':post_cnt,
                'friend_requests' : friend_requests,
                'current_users' : current_users,
                'friend_cnt' : friend_cnt,
                })
    else:
        not_exists = True
        return render(request, 'users/profile.html',{'user_posts' : user_posts, 
        'not_exists': not_exists, 
        'post_cnt':post_cnt,
        'friend_requests' : friend_requests,
        'current_users' : current_users,
        'friend_cnt' : friend_cnt,
        })

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
def u_profile(request, username, u_id):
    friend = False
    friend_of_user = Account.objects.filter(friends=u_id)
    user = User.objects.get(pk=u_id)
    posts = AddPost.objects.filter(account=u_id)
    post_cnt = AddPost.objects.filter(account=u_id).count
    friend_cnt = Account.objects.filter(friends=u_id).count
    if friend_of_user.exists():
        friend = True
    else:
        friend = False
    return render(request, 'users/u_profile.html', {'user' : user, 
                                                    'posts' : posts, 
                                                    'post_cnt' : post_cnt,
                                                    'friend_cnt' : friend_cnt,
                                                    'friend' : friend, 
                                                    })


@login_required
def send_friend_request(request, u_id):
    sender = request.user
    reciever = User.objects.get(pk=u_id)
    FriendRequest.objects.get_or_create(sender=sender, reciever=reciever)
    return redirect('profile')

@login_required
def accept_request(request, u_id):
    friend_request = FriendRequest.objects.get(pk=u_id) #looking for friend requests with the specific user id
    active_user = request.user #this is the active user logged in
    active_user.account.friends.add(friend_request.sender) #adds sender
    sender = friend_request.sender #this is the user who sent the FR
    sender.account.friends.add(active_user) #adds logged in user who accepted FR to friends list
    friend_request.delete()
    return redirect('friend-requests')

@login_required
def decline_request(request, u_id):
    friend_request = FriendRequest.objects.get(pk=u_id)
    friend_request.delete()
    return redirect('friend-requests')


@login_required
def friend_requests(request):
    exists = True
    friend_requests = FriendRequest.objects.filter(reciever=request.user)
    current_users = User.objects.exclude(username=request.user)
    if friend_requests.exists():
        return render(request,'users/friend_requests.html', {'friend_requests' : friend_requests, 'exists' : exists})
    else:
        exists = False
        return render(request,'users/friend_requests.html', {'friend_requests' : friend_requests, 'exists' : exists})

@login_required
def pending_friend_requests(request):
    sent_exists = True
    sent_friend_requests = FriendRequest.objects.filter(sender=request.user)
    current_users = User.objects.exclude(username=request.user)
    if sent_friend_requests.exists():
        return render(request,'users/pending_friend_requests.html', {'sent_friend_requests' : sent_friend_requests, 'sent_exists' : sent_exists,})
    else:
        sent_exists = False
        return render(request,'users/pending_friend_requests.html', {'sent_friend_requests' : sent_friend_requests, 'sent_exists' : sent_exists,})
    

    




