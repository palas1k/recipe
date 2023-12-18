import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from comments.models import Comments
from comments.serializers import CommentsSerializer
from posts.models import Post
from userprofile.models import Profile

pytestmark = pytest.mark.django_db


def test_get_comment(post):
    comment = baker.make(Comments, post=post)
    serializer = CommentsSerializer(comment)
    assert serializer.data


@pytest.mark.django_db
def test_post_comment(post):
    expected_data = {
        'text': 'Тестовый комментарий',
        'reply_for': None,
    }
    serializer = CommentsSerializer(expected_data)
    assert expected_data == serializer.data
