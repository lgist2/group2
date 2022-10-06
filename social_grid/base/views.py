from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from post.forms import AddPostForm
from django.views.generic import ListView, DetailView

from post.models import AddPost


# Create your views here.
@login_required
def home(request):
    context = {
        'posts' : AddPost.objects.all()
    }
    return render(request, 'base/home.html', context)


class PostListView(ListView):
    model = AddPost
    template_name = 'base/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = AddPost