from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from post.forms import AddPostForm


# Create your views here.
@login_required
def home(request):
    return render(request, 'base/home.html')
