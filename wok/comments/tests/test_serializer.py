import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from comments.models import Comments
from posts.models import Post
from userprofile.models import Profile

pytestmark = pytest.mark.django_db


def test_get_comment_unauth(client):
    post = baker.make(Post)
    com = baker.make(Comments, post=post)
    response = client.get(f"/api/v1/post/{post.pk}/comment/")
    assert 401 == response.status_code


@pytest.mark.django_db
def test_get_comment_auth(client):
    user = Profile.objects.create_user(username='test_username')
    client.force_authenticate(user)
    post = baker.make(Post)
    baker.make(Comments, post=post)
    response = client.get(f"/api/v1/post/{post.pk}/comment/")
    assert 200 == response.status_code
