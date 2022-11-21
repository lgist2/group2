from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from post.forms import PostForm, CommentForm
from django.contrib.auth.models import User
from users.models import Account, FriendRequest
from post.models import Post, RePost


# Create your views here.
@login_required
def home(request):
    #gets active user
    #filters the posts and displays only the posts of the users friends
    active_user = request.user
    users = User.objects.all()
    not_friends = Account.objects.exclude(friends=active_user).exclude(user=active_user)
    posts = Post.objects.filter(account__friends=active_user.account).order_by("-id")
    friends = Account.objects.filter(friends=active_user).exclude(user=active_user)
    reposts = RePost.objects.filter(new__friends=active_user.account).order_by("-id")
    liked = Post.objects.filter(likes=active_user)
    context = {
        'posts' : posts,
        'reposts' : reposts,
        'friends' : friends,
        'users' : users,
        'not_friends' : not_friends,
        'liked' : liked,
        'active_user' : active_user,
    }
    return render(request, 'base/home.html', context)


