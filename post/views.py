from django.shortcuts import render, redirect
from .models import AddPost
from .forms import AddPostForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


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
