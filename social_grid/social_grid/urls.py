"""social_grid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from post import views as post_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.registration, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/update-profile', user_views.update_profile, name='update-profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('base.urls')),
    path('create-post/', post_views.addpost, name='createpost'),
    path('update-post/<str:pk>/', post_views.updatepost, name='update-post'),
    path('delete-post/<str:pk>/', post_views.deletepost, name='delete-post'),
    path('search-user/', user_views.search_user, name='search-user'),
    path('user-profile/<str:u_id>', user_views.u_profile, name='user-profile'),
    path('add-friend/<str:u_id>/', user_views.send_friend_request, name='add-friend'),
    path('accept/<str:u_id>/', user_views.accept_request, name='accept'),
    path('decline/<str:u_id>/', user_views.decline_request, name='decline'),
    path('profile/friend-requests', user_views.friend_requests, name='friend-requests'),
    path('profile/pending-friend-requests', user_views.pending_friend_requests, name='pending-friend-requests'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
