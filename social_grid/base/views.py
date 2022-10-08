from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from post.forms import AddPostForm


from post.models import AddPost


# Create your views here.
@login_required
def home(request):
    context = {
        'posts' : AddPost.objects.all()
    }
    return render(request, 'base/home.html', context)


