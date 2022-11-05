from django.test import TestCase

# Create your tests here.

from post.models import Post, Comment
from users.models import Account

class PostModelTestCases(TestCase):

    @classmethod
    def setUpTestData(cls):
        Post.objects.create(title = 'Cool post title', hashtags = 'fyp')

    def test_title_max_length(self):
        post = Post.objects.get(id=1)   
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_hashtags_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('hashtags').max_length
        self.assertEqual(max_length, 50)
    
    def test_title_name(self):
        post = Post.objects.get(id=1)
        title = Post.objects.get(title = "Cool post title")
        self.assertEqual(title, 'Cool post title')




class CommentModelTestCases(TestCase):

    @classmethod
    def setupTestData(cls):
       
        Comment.objects.create(body = 'Very cool post!', created_on = 10/25/22)

    def test_body(self):
        comment = Comment.objects.get(id=1)
        body = Comment.objects.get(body = "Very cool post!")
        self.assertEqual(body, 'Very cool post!')

    def test_date_time(self):
        comment = Comment.objects.get(id=1)
        created_on = Comment.objects.get(created_on = 10/25/22)
        self.assertEqual(created_on, 10/25/22)





 