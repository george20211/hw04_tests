# static_pages/tests/test_urls.py
from django.shortcuts import redirect
from django.test import TestCase, Client
from posts.models import Group, Post
from django.contrib.auth import get_user_model


User = get_user_model()


class UrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='AndreyG')
        cls.post = Post.objects.create(
            text='TestText',
            author=cls.author,
        )

        Group.objects.create(
            title='test title',
            slug='test-slug'
        )

    def setUp(self):

        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)
        self.another_authorized_client = Client()
        self.another_authorized_client.force_login(
            User.objects.create_user(username='TEST_USR2'))

    def test_homepage_NON_auth(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200, 'err001')

    def test_homepage_auth(self):
        response = self.authorized_client.get('/')
        self.assertEqual(response.status_code, 200, 'err002')

    def test_template_index(self):
        response = self.authorized_client.get('/')
        self.assertTemplateUsed(response, 'index.html', 'err03')

    def test_group_page_auth(self):
        response = self.authorized_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200, 'err004')

    def test_group_page_NON_auth(self):
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200, 'err005')

    def test_template_group(self):
        response = self.authorized_client.get('/group/test-slug/')
        self.assertTemplateUsed(response, 'group.html', 'err06')

    def test_auth_user_add_post(self):
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200, 'err01')

    def test_template_add_post(self):
        response = self.authorized_client.get('/new/')
        self.assertTemplateUsed(response, 'new.html', 'err02')

    def test_NOT_auth_usr_add_post(self):
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 302, 'err03')

    def test_profile_user(self):
        response = self.guest_client.get('/AndreyG/')
        self.assertEqual(response.status_code, 200, 'err07')

    def test_profile_user_post(self):
        response = self.guest_client.get(f'/{ self.author }/{ self.post.id }/')
        self.assertEqual(response.status_code, 200, 'err08')

    def test_edit_post(self):
        response = self.guest_client.get(
            f'/{ self.author }/{ self.post.id }/edit/')
        self.assertEqual(response.status_code, 302, 'err08')

        response = self.authorized_client.get(
            f'/{ self.author }/{ self.post.id }/edit/')
        self.assertEqual(response.status_code, 200, 'err09')

        response = self.another_authorized_client.get(
            f'/{ self.author.username }/{ self.post.id }/edit/')
        self.assertTemplateUsed(response, 'error.html', 'err10')
