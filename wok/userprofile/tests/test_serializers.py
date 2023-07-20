from django.test import TestCase

from userprofile.serializers import ProfileSerializer
from userprofile.models import Profile


class ProfileSerializerTestCase(TestCase):
    def test_user(self):
        user1 = Profile.objects.create(avatar=None, username='user1')
        user2 = Profile.objects.create(username='user2', avatar=None)
        data = ProfileSerializer([user1, user2], many=True).data
        print(data)
        # expected_data = [
        #     {
        #         'id': user1.id,
        #         'username': 'user1'
        #     },
        #     {
        #         'id': user2.id,
        #         'username': 'user2'
        #     },
        # ]
        # self.assertEqual(expected_data, data)
