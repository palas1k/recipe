import json
from collections import OrderedDict

from django.db.models import CharField
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.serializers import ValidationError

from userprofile.serializers import ProfileSerializer, ChangePasswordSerializer, SignUpSerializer

from userprofile.models import Profile


class UserSerializerTestCase(TestCase):
    def test_user(self):
        user1 = Profile.objects.create(username='user1')
        user2 = Profile.objects.create(username='user2')
        data = ProfileSerializer([user1, user2], many=True).data
        expect_data = [
            OrderedDict([('username', 'user1'), ('avatar', None)]),
            OrderedDict([('username', 'user2'), ('avatar', None)])
        ]
        self.assertEqual(2, len(data))
        self.assertEqual(expect_data, data)


class ProfileSerializerTestCase(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create_user(username='user1')
        self.data = ProfileSerializer(self.profile).data

    def test_profile(self):
        expected_data = {'avatar': None, 'username': 'user1'}
        self.assertEqual(expected_data, self.data)


class ChangePasswordSerializerTestCase(TestCase):
    def test_fields(self):
        data = ChangePasswordSerializer().data
        expected_data = {'old_password': '', 'new_password': ''}
        # expected_data = []
        self.assertEqual(expected_data, data)


class SignUpSerializerTestCase(TestCase):
    def test_fields(self):
        data = SignUpSerializer().data
        expected_data = {'username': '', 'password': '', 'password2': ''}
        self.assertEqual(expected_data, data)

    def test_validate(self):
        serializer = SignUpSerializer(data={'password': 'password'})
        with self.assertRaises(ValidationError):
            serializer.validate_password2('password2')
        self.assertEqual('password', serializer.validate_password2('password'))
