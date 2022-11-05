from django.test import TestCase
from users.models import Account
from users.models import FriendRequest

# Create your tests here.

class AccountModelTestCases(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Account.objects.create(user = models.OneToOneField(User, on_delete=models.CASCADE), bio = 'Testing if the bio feature works', posts_liked = 2)  
    
    def test_username(self):
        account = Account.objects.get(id=1)
        user = Account.objects.get(user = 'Tenshi')
        self.assertEqual(user, 'Tenshi')
        
    def test_bio(self):
        account = Account.objects.get(id=1)
        bio = Account.objects.get(bio = 'Testing if bio feature works')
        self.assertEqual(bio, 'Testing if bio feature works')

    #def test_profilePic(self):

    def test_postsLiked(self):
        account = Account.objects.get(id=1)
        posts_liked = Account.objects.get(posts_liked = 2)
        self.assertEqual(posts_liked, 2)

class FriendRequestModelTestCases(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        FriendRequest.objects.create(sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender'), receiver = models.ForeignKey(User, on_delete=models.CASCADE, is_active = True, timestamp = '10/25/22')

    def test_Sender(self):
        request = FriendRequest.objects.get(id=1)
        sender = FriendRequest.objects.get(sender = 'Tenshi')
        self.assertEqual(sender, 'Tenshi')

    def test_Receiver(self):
        request = FriendRequest.objects.get(id=1)
        receiver = FriendRequest.objects.get(sender = 'mrflam')
        self.assertEqual(receiver, 'mrflam')

    def test_Active(self):
        request = FriendRequest.objects.get(id=1)
        is_active = FriendRequest.objects.get(is_active = True)
        self.assertEqual(is_active, True)

    def test_Timestamp(self):
        request = FriendRequest.objects.get(id=1)
        timestamp = FriendRequest.objects.get(timestamp = '10/25/22')
        self.assertEqual(timestamp, '10/25/22')