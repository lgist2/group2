from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from post.forms import AddPostForm
from django.contrib.auth.models import User
from users.models import Account, FriendRequest


from post.models import AddPost


# Create your views here.
@login_required
def home(request):
    #gets active user
    #filters the posts and displays only the posts of the users friends
    active_user = request.user
    posts = AddPost.objects.filter(account__friends=active_user.account)
    context = {
        'posts' : posts, 
    }
    return render(request, 'base/home.html', context)


