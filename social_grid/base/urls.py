from django.urls import path
from . import views as base_views

urlpatterns = [
    path('', base_views.home, name='home-page'),
]
#path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail')