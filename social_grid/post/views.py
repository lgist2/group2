from django.shortcuts import render, redirect

from users.models import Account
from django.contrib.auth.models import User
from .models import AddPost
from .forms import AddPostForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy


def addpost(request):
    new_post = False
    form = AddPostForm()
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.account = request.user
            instance.save()
            return HttpResponseRedirect('/create-post?new_post=True')
    else:
        form = AddPostForm()
        if 'new_post' in request.GET:
            new_post = True
    return render(request, 'post/create_post.html', {'form': form, 'new_post': new_post})
 
def updatepost(request, pk):
    post = AddPost.objects.get(id=pk)
    form = AddPostForm(instance=post)
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'post/update_post.html', {'form': form, 'post' : post,})

def deletepost(request,pk):
    post = AddPost.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect('profile')
    return render(request, 'post/delete_post.html',{'item':post})


def like_post(request, username, p_id):
    post = AddPost.objects.get(id=p_id)
    post.likes.add(request.user)
    active_user = request.user
    active_user.account.posts_liked.add(post)
    return redirect('home-page')
