import json
from collections import OrderedDict

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from rest_framework.test import force_authenticate, APITestCase

from post_create.models import Post, PostContent
from post_create.serializers import PostSerializer, AllPostsSerializer


class PostRetrieveAPIViewTestCase(APITestCase):
    def setUp(self):
        self.post1 = Post.objects.create(title='post1')
        self.post2 = Post.objects.create(title='post2')
        self.user = User.objects.create(username='user')
        self.url = reverse('post-detail', args={self.post1.id})

    def test_get_authenticated(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        expected_data = PostSerializer(self.post1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_get_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_staff_authenticated(self):
        user1 = User.objects.create(username='user1', is_staff=True)
        self.client.force_authenticate(user1)
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, Post.objects.all().count())

    def test_delete_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_delete_owner(self):
        user2 = User.objects.create(username='user2')
        post3 = Post.objects.create(title='post3', author=user2)
        url = reverse('post-detail', args={post3.id})
        self.client.force_authenticate(user2)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, Post.objects.all().count())

    def test_patch_unauthenticated(self):
        response = self.client.patch(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_patch_is_staff(self):
        user1 = User.objects.create(username='user1', is_staff=True)
        self.client.force_authenticate(user1)
        data = {
            'title': 'tested'
        }
        json_data = json.dumps(data)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        self.post1.refresh_from_db()
        expected_data = PostSerializer(self.post1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_patch_owner(self):
        user = User.objects.create(username='user2')
        post = Post.objects.create(title='test', author=user)
        self.client.force_authenticate(user)
        url = reverse('post-detail', args={post.id})
        data = {
            'title': 'tested'
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        post.refresh_from_db()
        expected_data = PostSerializer(post).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)


class AllPostsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.post1 = Post.objects.create(title='post1')
        self.post2 = Post.objects.create(title='post2')
        self.user = User.objects.create(username='user')
        self.url = reverse('posts')

    def test_get_unauth(self):
        response = self.client.get(self.url)
        data = AllPostsSerializer([self.post1, self.post2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data, response.data['results'][::-1])

    def test_get_auth(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        data = AllPostsSerializer([self.post1, self.post2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data, response.data['results'][::-1])


class CreatePostAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.url = reverse('post-create')
        self.data = {"title": "title",
                     "post_content":
                         [
                             {
                                 "text": "string",
                                 "image": "null"
                             },
                         ]
                     }
        self.json_data = json.dumps(self.data)

    def test_post_auth(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Post.objects.all().count())

    def test_post_unauth(self):
        response = self.client.post(self.url, data=self.json_data, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_post_many_post_content(self):
        self.client.force_authenticate(self.user)
        data = {"title": "title",
                "post_content":
                    [
                        {
                            "text": "string",
                            "image": "null"
                        },
                        {
                            "text": "string",
                            "image": "null"
                        },
                        {
                            "text": "string",
                            "image": "null"
                        }
                    ]
                }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, PostContent.objects.all().count())
        self.assertEqual(1, Post.objects.all().count())

    def test_wrong_fields(self):
        self.client.force_authenticate(self.user)
        data = {"title": "title",
                "post_content":
                    [
                        {
                            "text": "!@@!#!da",
                            "image": None
                        }
                    ]
                }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
