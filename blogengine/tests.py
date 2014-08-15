from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post

class PostTest(TestCase):
    def test_create_post(self):
        post = Post()

        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()

        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        self.assertEquals(only_post.title, 'My first post')
        self.assertEquals(only_post.text, 'This is my first blog post')
        self.assertEquals(only_post.pub_date.day, post.pub_date.day)
        self.assertEquals(only_post.pub_date.month, post.pub_date.month)
        self.assertEquals(only_post.pub_date.year, post.pub_date.year)
        self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEquals(only_post.pub_date.second, post.pub_date.second)

class AdminTest(LiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        # This automatically runs when the test runs
        self.client = Client()

    def test_login(self):
        # Get login page
        response = self.client.get('/admin/')
        # Check response code
        self.assertEquals(response.status_code, 200)
        # Log in should be in the string content response
        self.assertTrue('Log in' in response.content)
        # Log the user in
        self.client.login(username='zelda', password='password')
        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        # Log in
        self.client.login(username='zelda', password='password')
        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        # Check for 'Log out' in response
        self.assertTrue('Log out' in response.content)
        self.client.logout() # Logout
