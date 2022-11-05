from django.test import TestCase
from users.models import Account
from users.models import FriendRequest

# Create your tests here.

class AccountModelTestCases(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Account.objects.create(user = models.OneToOneField(User, on_delete=models.CASCADE), bio = 'Testing if the bio feature works')  
    
    def test_username(self):
        account = Account.objects.get(id=1)
        user = Account.objects.get(user = 'TestUser1')
        self.assertEqual(user, 'TestUser1')
        
    def test_bio(self):
        account = Account.objects.get(id=1)
        bio = Account.objects.get(bio = 'Testing if bio feature works')
        self.assertEqual(bio, 'Testing if bio feature works')

    #def test_profilePic(self):

class FriendRequestModelTestCases(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        FriendRequest.objects.create(sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender'))