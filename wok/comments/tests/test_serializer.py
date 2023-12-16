import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from comments.models import Comments
from posts.models import Post

pytestmark = pytest.mark.django_db


def test_get_comment(user, client):
    client.force_login(user)
    baker.make(Comments)
    response = client.get("api/v1/post/1/comment/")
    assert 200 == response.status_code
