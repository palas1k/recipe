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
        # self.client.force_authenticate(self.user1)
        # data = {
        #     "user": {"username": "user2"}
        # }
        # json_data = json.dumps(data)
        # response = self.client.patch(self.url, data=json_data, content_type='application/json')
        # self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.assertEqual({'avatar': None, 'user': OrderedDict([('username', 'user2')])}, response.data)
        pass

    def test_get_my_profile_staff(self):
        staff = User.objects.create(username='staff', is_staff=True)
        self.client.force_authenticate(staff)
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'avatar': None, 'user': 'staff'}, response.data)


class ChangePasswordAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user1.set_password('string')
        self.url = reverse('password-update')
        self.data = {
            'old_password': 'string',
            'new_password': 'password'
        }
        self.json_data = json.dumps(self.data)

    def test_change_password_authorized(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url, data=self.json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'message': 'Password updated successfully'}, response.data)
        self.assertTrue(self.client.login(username='user1', password='password'))

    def test_change_password_unauthorized(self):
        response = self.client.post(self.url, data=self.json_data, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_change_password_wrong_old_password(self):
        data = {
            'old_password': 'wrong',
            'new_password': 'password'
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual({"old_password": ["Wrong password"]}, response.data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_change_password_staff(self):
        user = User.objects.create(username='staff', is_staff=True)
        user.set_password('string')
        self.client.force_authenticate(user)
        response = self.client.post(self.url, data=self.json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(self.client.login(username='staff', password='password'))

    def test_data_not_valid(self):
        data = {
            'old_password': 'string',
            'new_password': ''
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class SignUpAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('signup')
        data = {
            'username': 'user',
            'password': 'password',
            'password2': 'password'
        }
        self.json_data = json.dumps(data)

    def test_signup(self):
        response = self.client.post(self.url, self.json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(self.client.login(username='user', password='password'))

    def test_signup_passwords_not_equal(self):
        data = {
            'username': 'user',
            'password': 'password',
            'password2': 'password1'
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_signup_password_user_exists(self):
        self.client.post(self.url, self.json_data, content_type='application/json')
        data = {
            'username': 'user',
            'password': 'password',
            'password2': 'password1'
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
