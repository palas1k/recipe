import json
from collections import OrderedDict

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import force_authenticate, APITestCase

from userprofile.serializers import ProfileSerializer
from userprofile.models import Profile


class GetProfileAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.profile = Profile.objects.get(user=self.user1)

    def test_get_profile_unauthorized(self):
        url = reverse('profile', args=(self.user1.id,))
        response = self.client.get(url)
        serializer_data = ProfileSerializer(self.profile).data
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_profile_authorized(self):
        self.client.force_authenticate(self.user2)
        url = reverse('profile', args=(self.user1.id,))
        response = self.client.get(url)
        serializer_data = ProfileSerializer(self.profile).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_profile_staff(self):
        user3 = User.objects.create(username='user3', is_staff=True)
        self.client.force_authenticate(user3)
        url = reverse('profile', args=(self.user1.id,))
        response = self.client.get(url)
        serializer_data = ProfileSerializer(self.profile).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class GetMyProfileAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.profile = Profile.objects.get(user=self.user1)
        self.url = reverse('my-profile')

    def test_get_my_profile_authorized(self):
        self.client.force_authenticate(self.user1)
        self.response = self.client.get(self.url)
        serializer_data = ProfileSerializer(self.profile).data
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)
        self.assertEqual(serializer_data, self.response.data)

    def test_get_my_profile_unauthorized(self):
        self.response = self.client.get(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self.response.status_code)

    def test_delete_my_profile_authorized(self):
        self.client.force_authenticate(self.user1)
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, User.objects.all().count())

    def test_patch_my_profile(self):
        self.client.force_authenticate(self.user1)
        data = {
            'username': 'user2'
        }
        json_data = json.dumps(data)
        response = self.client.patch(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'avatar': None, 'user': OrderedDict([('username', 'user2')])}, response.data)

    def test_get_my_profile_staff(self):
        staff = User.objects.create(username='staff', is_staff=True)
        self.client.force_authenticate(staff)
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'avatar': None, 'user': OrderedDict([('username', 'staff')])}, response.data)
