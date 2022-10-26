from django.contrib import admin
<<<<<<< HEAD
from .models import Account

admin.site.register(Account)
#admin.site.register(Relationship)
=======
from .models import Account, FriendRequest

admin.site.register(Account)
#admin.site.register(FriendList)
admin.site.register(FriendRequest)
>>>>>>> Levi-Branch
