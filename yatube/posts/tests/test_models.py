from django.test import TestCase
from ..models import Post, Group, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        author = User.objects.create_user(username='TEST_USR')
        cls.Post = Post.objects.create(
            text="тестовыйпостна15символов",
            author=author,)
        cls.Group = Group.objects.create(
            title="test")

    def test_object_name_is_title_field(self):
        group = PostModelTest.Group
        groups = group.title
        self.assertEqual(groups, "test")

    def test_object_name_title_have_15_symbols(self):
        post = PostModelTest.Post
        post = post.text[:15]
        self.assertEqual(post, "тестовыйпостна1")
