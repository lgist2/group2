from asyncio.windows_events import NULL
from tkinter import E
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

from .models import Account, FriendRequest
from post.models import SharePost
from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm
from django.contrib.auth.decorators import login_required
from post.models import Post, RePost


def registration(request):   
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username +'! Please login below.')
            
             #need to add message to html instead
            #Relationship.objects.create(user=user,)
            Account.objects.create(user=user,) #creates a profile account for the new user
            user.account.friends.add(user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout_check(request):
    return render(request, 'users/logout_check.html', {})

@login_required()
def profile(request):
    
    not_exists = False
    active_account = Post()
    active_account.account = request.user
    current_posts = Post.objects.all()
    user_posts = Post.objects.filter(account=active_account.account).order_by("-id")
    reposts = RePost.objects.filter(new=active_account.account).order_by("-id")
    post_cnt = Post.objects.filter(account=active_account.account).count
    friend_cnt = Account.objects.filter(friends=active_account.account).exclude(user=active_account.account).count
    friend_requests = FriendRequest.objects.filter(receiver=request.user)
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
                'reposts' : reposts,
                })
            else:
                return render(request, 'users/profile.html', {'user_posts' : user_posts,
                'not_exists': not_exists, 
                'post_cnt':post_cnt,
                'friend_requests' : friend_requests,
                'current_users' : current_users,
                'friend_cnt' : friend_cnt,
                'reposts' : reposts,
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
    real = False
    if request.method == 'POST':
        search = request.POST['search']
        users = User.objects.filter(username__contains=search) | User.objects.filter(first_name__contains=search) | User.objects.filter(last_name__contains=search)
        if users.exists():
            real = True
        current_user = request.user
        return render(request, 'users/search_user.html', {'search' : search, 'users' : users, 'current_users' : current_user, 'real' : real,})
    else:
        return render(request, 'users/search_user.html', {'search' : search, 'users' : users, 'current_users' : current_user, 'real' : real,})

@login_required
def u_profile(request, username, u_id):
    friend_of_user = False
    active_account = request.user
    user = User.objects.get(pk=u_id)
    friends = Account.objects.filter(friends=active_account)
    posts = Post.objects.filter(account=u_id).order_by("-id")
    post_cnt = Post.objects.filter(account=u_id).count
    friend_cnt = Account.objects.filter(friends=u_id).exclude(user=u_id).count
    for friend in friends:
        if friend == user.account:
            friend_of_user = True
    return render(request, 'users/u_profile.html', {'user' : user, 
                                                    'posts' : posts, 
                                                    'post_cnt' : post_cnt,
                                                    'friend_cnt' : friend_cnt,
                                                    'friend_of_user' : friend_of_user,
                                                    })


@login_required
def send_friend_request(request, u_id):
    sender = request.user
    receiver = User.objects.get(pk=u_id)
    messages.success(request, 'Friend request sent!')
    FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
    return redirect('profile')

@login_required
def accept_request(request, u_id):
    friend_request = FriendRequest.objects.get(pk=u_id) #looking for friend requests with the specific user id
    active_user = request.user #this is the active user logged in
    active_user.account.friends.add(friend_request.sender) #adds sender
    sender = friend_request.sender #this is the user who sent the FR
    sender.account.friends.add(active_user) #adds logged in user who accepted FR to friends list
    friend_request.delete()
    messages.success(request, 'Friend request accepted!')
    return redirect('friend-requests')

@login_required
def decline_request(request, u_id):
    friend_request = FriendRequest.objects.get(pk=u_id)
    friend_request.delete()
    messages.success(request, 'Friend request Declined!')
    return redirect('friend-requests')

@login_required
def remove_friend(request, u_id):
    unactive_user = Account.objects.get(user=u_id)
    active_user = request.user
    active_user.account.friends.remove(u_id)
    unactive_user.friends.remove(active_user)
    messages.success(request, 'Friend removed!')
    return redirect('profile')


@login_required
def notifications(request):
    exists = False
    private = True
    friend_requests = FriendRequest.objects.filter(receiver=request.user)
    posts_shared = SharePost.objects.filter(receiver=request.user)
    current_users = User.objects.exclude(username=request.user)
    context = {
        'friend_requests' : friend_requests,
        'posts_shared': posts_shared,
        'exists' : exists, 
        'private' : private,
    }
    if friend_requests.exists() or posts_shared.exists():
        exists = True
        return render(request,'users/notifications.html', context)
    else:
        return render(request,'users/notifications.html', context)

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
    

@login_required
def all_friends(request):
    has_friends = True
    friends = Account.objects.filter(friends=request.user).exclude(user=request.user)
    if friends.exists():
        return render(request,'users/all_friends.html', {'friends' : friends, 'has_friends' : has_friends})
    else:
        has_friends = False
        return render(request,'users/all_friends.html', {'friends' : friends, 'has_friends' : has_friends})

@login_required
def all_suggestions(request):
    has_friends = True
    active_user = request.user
    not_friends = Account.objects.exclude(friends=active_user).exclude(user=active_user)
    if not_friends.exists():
        return render(request,'users/all_suggestions.html', {'not_friends' : not_friends, 'has_friends' : has_friends})
    else:
        has_friends = False
        return render(request,'users/all_suggestions.html', {'not_friends' : not_friends, 'has_friends' : has_friends})

@login_required
def reposts(request):
    has_reposts = True
    active_user = request.user
    reposts = RePost.objects.filter(new=active_user).order_by('-id')
    if reposts.exists():
        return render(request,'users/reposts.html', {'reposts' : reposts, 'has_reposts' : has_reposts})
    else:
        has_reposts = False
        return render(request,'users/reposts.html', {'reposts' : reposts, 'has_reposts' : has_reposts})




