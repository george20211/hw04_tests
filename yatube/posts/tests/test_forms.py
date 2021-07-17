from django.test import Client, TestCase
from django.urls import reverse
from ..forms import PostForm
from ..models import Post, User


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='AndreyG')
        cls.post = Post.objects.create(
            text='текст',
            author=cls.author,
        )

        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_add_post(self):
        counter = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
        }
        self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )

        self.assertEqual(Post.objects.count(), counter + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
            ).exists()
        )

    def test_edit_post(self):
        form_data = {'text': 'ИзменилТекст'}
        response = self.authorized_client.post(
            reverse('post_edit', kwargs={"username": self.author.username,
                    "post_id": self.post.id}),
            data=form_data)
        z = Post.objects.get(id=self.post.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(z.text, 'ИзменилТекст')
