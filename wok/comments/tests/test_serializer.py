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


def test_post_comment():
    expected_data = {
        'text': 'Тестовый комментарий',
        'reply_for': None,
    }
    serializer = CommentsSerializer(expected_data)
    assert expected_data == serializer.data


def test_post_reply(comment_with_post):
    expected_data = {
        'text': 'Тестовый комментарий',
        'reply_for': comment_with_post,
    }
    data = CommentsSerializer(expected_data).data
    print(data)
    print(expected_data)
    assert expected_data['text'] == data['text']
    assert comment_with_post.pk == data['reply_for']


def test_fields(comment_with_post):
    data = CommentsSerializer(comment_with_post).data
    assert 3 == len(data)
