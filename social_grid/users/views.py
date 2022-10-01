from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from post.models import AddPost


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You now can login!') #need to add to html instead 
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required()
def profile(request):
    not_exists = False
    active_account = AddPost()
    active_account.account = request.user
    current_posts = AddPost.objects.all()
    user_posts = AddPost.objects.filter(account=active_account.account)
    if current_posts.exists():
        for posts in current_posts:
            if user_posts == posts.account:
                return render(request, 'users/profile.html', {'user_posts' : user_posts, 'not_exists': not_exists})
            else:
                return render(request, 'users/profile.html', {'user_posts' : user_posts, 'not_exists': not_exists})
    else:
        not_exists = True
        return render(request, 'users/profile.html',{'user_posts' : user_posts, 'not_exists': not_exists})