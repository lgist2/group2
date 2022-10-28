from django.shortcuts import render, redirect

from users.models import Account
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy


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
    post.likes.add(request.user)
    active_user = request.user
    active_user.account.posts_liked.add(post)
    return redirect('home-page')

def unlike_post(request, username, p_id):
    post = Post.objects.get(id=p_id)
    post.likes.remove(request.user)
    active_user = request.user
    active_user.account.posts_liked.remove(post)
    return redirect('home-page')


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
            return redirect('home-page')
    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'post/comment_on_post.html', context)


def post_comments(request, p_id):
    has_likes = False
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
    }
    return render(request, 'post/post_comments.html', context)
