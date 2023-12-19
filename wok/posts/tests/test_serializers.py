from collections import OrderedDict

from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from posts.models import Post, PostContent
from posts.serializers import PostContentSerializer, PostSerializer, AllPostsSerializer, CreatePostSerializer
from userprofile.models import Profile


class PostContentSerializerTestCase(TestCase):
    def test_post_content_create(self):
        post = Post.objects.create(title='тестовый')
        user = Profile.objects.create(username='user')
        # self.client.force_login(user)
        post_conten1 = PostContent(text='post_content1', post=post)
        post_conten2 = PostContent(text='post_content2', post=post)
        data = PostContentSerializer([post_conten1, post_conten2], many=True).data
        expected_data = [OrderedDict([('text', 'post_content1'), ('image', None)]),
                         OrderedDict([('text', 'post_content2'), ('image', None)])]
        self.assertEqual(expected_data, data)


class PostSerializerTestCase(TestCase):
    def test_post_create(self):
        post = Post.objects.create(title='тест1')
        data = PostSerializer(post).data
        self.assertEqual(16, len(data.values()))


class AllPostsSerializerTestCase(TestCase):
    def test_get_all_posts(self):
        post1 = Post.objects.create(title='test1')
        post2 = Post.objects.create(title='test2')
        # data = AllPostsSerializer([post1, post2], many=True).data
        data2 = AllPostsSerializer().data
        self.assertEqual(1, len(data2))


class CreatePostSerializerTestCase(TestCase):
    def test_create_post(self):
        data = CreatePostSerializer().data
        expected_data = {'title': '', 'post_content': []}
        self.assertEqual(expected_data, data)
