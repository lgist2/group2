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

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html"), name='password_reset'), 
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),#success email sent
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout_check/', user_views.logout_check, name='logout_check'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('', include('base.urls')),

    path('create-post/', post_views.addpost, name='createpost'),
    path('update-post/<str:pk>/', post_views.updatepost, name='update-post'),
    path('delete-post/<str:pk>/', post_views.deletepost, name='delete-post'),

    path('like-post/?=user=<str:username>/?=post<str:p_id>/', post_views.like_post, name='like-post'),
    path('unlike-post/?=user=<str:username>/?=post<str:p_id>/', post_views.unlike_post, name='unlike-post'),
    path('comment-on-post/?=post<str:p_id>/', post_views.comment_on_post, name='comment-post'),
    path('post-details/?=post<str:p_id>/', post_views.post_details, name='post-details'),
    path('share-post-to/?=post=<str:p_id>/', post_views.share_post_to, name='share-post-to'),
    path('share-post/?=user=<str:u_id>/?=post=<str:p_id>/', post_views.share_post, name='share-post'),
    path('delete/?=<str:u_id>/', post_views.delete_shared_post, name='delete-shared-post'),
    path('repost/?=<str:p_id>/?=<str:u_id>/', post_views.repost, name='repost'),
    path('post-shared/?=post<str:p_id>/', post_views.shared_posts, name='shared-posts'),


    path('search-user/', user_views.search_user, name='search-user'),
    path('user-profile/?=user=<str:username>/?=<str:u_id>', user_views.u_profile, name='user-profile'),
    path('add-friend/<str:u_id>/', user_views.send_friend_request, name='add-friend'),
    path('remove-friend//?=<str:u_id>', user_views.remove_friend, name='remove-friend'),
    path('accept/<str:u_id>/', user_views.accept_request, name='accept'),
    path('decline/<str:u_id>/', user_views.decline_request, name='decline'),
    path('profile/friend-requests', user_views.notifications, name='friend-requests'),
    path('profile/pending-friend-requests', user_views.pending_friend_requests, name='pending-friend-requests'),
    path('all-friends/', user_views.all_friends, name='all-friends'),
    path('all-suggestions/', user_views.all_suggestions, name='all-suggestions'),
    path('liked-posts/', post_views.posts_liked, name='posts-liked'),
    path('reposts/', user_views.reposts, name='reposts'),
    path('commented-posts/', post_views.posts_commented, name='posts-commented'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
