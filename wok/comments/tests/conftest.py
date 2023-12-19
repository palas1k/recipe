import pytest
from model_bakery import baker

from django.contrib.auth.models import User

from rest_framework.test import APIClient

from comments.models import Comments
from posts.models import Post
from userprofile.models import Profile


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def testuser():
    return Profile.objects.create(username='user1')

@pytest.fixture()
def auth(testuser, client):
    return client.force_authenticate(testuser)


@pytest.fixture()
def post():
    return baker.make(Post)


@pytest.fixture()
def url(post):
    return f"/api/v1/post/{post.pk}/comment/"


@pytest.fixture()
def comment():
    return baker.make(Comments)


@pytest.fixture()
def comment_with_post(post):
    return baker.make(Comments, post=post)
