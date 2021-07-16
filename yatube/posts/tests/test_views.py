from ..forms import PostForm
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from posts.models import Group, Post
from posts.urls import *
from ..models import *
from django.shortcuts import redirect


User = get_user_model()


class UrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='AndreyG')
        cls.post = Post.objects.create(
            text='TestText',
            author=cls.author,
            group=Group.objects.create(
                title='testGroup',
                slug='test-slug2',)
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

    def test_pages_uses_correct_template(self):
        templates_page_names = {
            'index.html': reverse('index'),
            'new.html': reverse('new_post'),
            'group.html': (
                reverse('group_posts', kwargs={'slug': 'test-slug'})
            ),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_group_page(self):
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug'})
            )
        self.assertEqual(response.context['group'].title, 'test title')
        self.assertEqual(response.context['group'].slug, 'test-slug')

    def test_page_index(self):
        response = self.authorized_client.get(
            reverse('index',))
        self.assertEqual(response.context['page'][0].text, 'TestText')

    def test_new_post_page(self):
        response = self.authorized_client.get(
            reverse('new_post'))
        form_fields = PostForm
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], form_fields)

    def test_edit_post_page(self):
        response = self.authorized_client.get(
            f'/{ self.author }/{ self.post.id }/edit/')
        form_fields = PostForm
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], form_fields)

    def test_profile_context(self):
        response = self.authorized_client.get(
            reverse('profile', kwargs={'username': f'{self.author}'}))
        self.assertEqual(response.context['page'][0].text, 'TestText')
        self.assertEqual(response.context['profile'].username, 'AndreyG')

    def test_post_in_right_group(self):
        response = self.guest_client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug2'}))
        self.assertEqual(response.context['page'][0].text, 'TestText')

        response = self.guest_client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug'}))
        with self.assertRaises(IndexError):
            response.context['page'][0].text

        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(response.context['page'][0].text, 'TestText')

    def test_about(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/tech.html', 'err06')

        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/author.html', 'err06')


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
                title='testGroup',
                slug='test-slug2',)
        cls.author = User.objects.create_user(username='TEST_USR')
        for _ in range(13):
            Post.objects.create(
                text='TestText', author=cls.author, group=cls.group,)

    def setUp(self):
        self.client = Client()

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_three_records(self):
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)

    def test_group_10post(self):
        response = self.client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug2'}))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_profile_10post(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': f'{self.author}'}))
        self.assertEqual(len(response.context.get('page').object_list), 5)
