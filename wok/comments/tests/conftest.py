import pytest
from model_bakery import baker

from django.contrib.auth.models import User

from rest_framework.test import APIClient

from posts.models import Post
from userprofile.models import Profile


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def testuser():
    return Profile.objects.create(username='user1')


# @pytest.fixture()
# def post():
#     return baker.make(Post)
