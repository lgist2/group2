from django.contrib import admin
from .models import Account, FriendRequest

admin.site.register(Account)
#admin.site.register(FriendList)
admin.site.register(FriendRequest)
