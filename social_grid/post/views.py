from django.shortcuts import render, redirect

from users.models import Account
from django.contrib.auth.models import User
from .models import Post, Comment, SharePost, RePost
from django.contrib import messages
from .forms import CommentForm, PostForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse


def addpost(request):
    new_post = False
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.account = request.user
            instance.save()
            return HttpResponseRedirect('/create-post?new_post=True')
    else:
        form = PostForm()
        if 'new_post' in request.GET:
            new_post = True
    return render(request, 'post/create_post.html', {'form': form, 'new_post': new_post})
 
def updatepost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'post/update_post.html', {'form': form, 'post' : post,})

def deletepost(request,pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect('profile')
    return render(request, 'post/delete_post.html',{'item':post})


def like_post(request, username, p_id):
    post = Post.objects.get(id=p_id)
    active_user = request.user
    if request.method == "POST":
        if active_user in post.likes.all():
            post.likes.remove(request.user)
            active_user.account.posts_liked.remove(post)
            val = 'Unlike'
        else:
            post.likes.add(request.user)
            active_user.account.posts_liked.add(post)
            val = 'Like'

        data = {
            'value' : val,
            'likes' : post.likes.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect('home-page')

""" def unlike_post(request, username, p_id):
    post = Post.objects.get(id=p_id)
    active_user = request.user
    if request.method == "POST":
        post.likes.remove(request.user)
        active_user.account.posts_liked.remove(post)
        val = "unlike"
        data = {
            'value' : val,
            'likes' : post.likes.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect('home-page') """


def comment_on_post(request, p_id):
    post = Post.objects.get(id=p_id)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.account = request.user
            instance.post = post
            instance.save()
            messages.success(request, 'Comment added!')
            return redirect('post-details', p_id)
    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'post/comment_on_post.html', context)


def post_details(request, p_id):
    has_likes = False
    is_friends = False
    post = Post.objects.get(id=p_id)
    likes = post.likes.all()
    comments = Comment.objects.filter(post=p_id)
    if likes.exists():
        has_likes = True
        
    context = {
        'post' : post,
        'comments' : comments,
        'likes' : likes,
        'has_likes' : has_likes,
        'is_friends' : is_friends,
    }
    return render(request, 'post/post_details.html', context)

def posts_liked(request):
    active_user = request.user
    posts = Post.objects.filter(likes=active_user)
    context = {
        'posts' : posts, 
    }
    return render(request, 'post/posts_liked.html', context)

def posts_commented(request):
    active_user = request.user
    comments = Comment.objects.filter(account=active_user)
    context = {
        'comments' : comments, 
    }
    return render(request, 'post/posts_commented.html', context)

@login_required
def share_post_to(request, p_id):
    post = Post.objects.get(pk=p_id)
    has_friends = True
    friends = Account.objects.filter(friends=request.user).exclude(user=request.user)
    if friends.exists():
        return render(request,'post/share_post_to.html', {'post' : post,'friends' : friends, 'has_friends' : has_friends})
    else:
        has_friends = False
        return render(request, 'post/share_post_to.html', {'post': post, 'friends' : friends, 'has_friends' : has_friends})

@login_required
def share_post(request, u_id, p_id):
    sender = request.user
    receiver = User.objects.get(pk=u_id)
    post = Post.objects.get(pk=p_id)
    messages.success(request, 'Post Shared!')
    SharePost.objects.get_or_create(sender=sender, receiver=receiver, post=post)
    return redirect('profile')

@login_required
def delete_shared_post(request, u_id):
    post_shared = SharePost.objects.get(pk=u_id)
    post_shared.delete()
    messages.success(request, 'Shared post deleted')
    return redirect('friend-requests')

@login_required
def shared_posts(request):
    exists = True
    posts = SharePost.objects.filter(receiver=request.user)
    current_users = User.objects.exclude(username=request.user)
    if posts.exists():
        return render(request,'users/friend_requests.html', {'posts' : posts, 'exists' : exists})
    else:
        exists = False
        return render(request,'users/friend_requests.html', {'posts' : posts, 'exists' : exists})

@login_required
def repost(request, p_id, u_id):
    post = Post.objects.get(pk=p_id)
    new = request.user
    original = User.objects.get(pk=u_id)
    RePost.objects.get_or_create(post=post, new=new, original=original)
    return redirect('reposts')


    
