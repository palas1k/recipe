import pytest
from model_bakery import baker

from comments.models import Comments
from comments.serializers import CommentsSerializer
from posts.models import Post

pytestmark = pytest.mark.django_db


def test_get_unauth(client, comment_with_post, url):
    response = client.get(url)
    assert 401 == response.status_code


def test_get_auth(testuser, client, comment_with_post, url):
    client.force_authenticate(testuser)
    response = client.get(url)
    data = {
        'text': comment_with_post.text,
        'reply_for': None,
    }
    assert 200 == response.status_code
    expected_data = CommentsSerializer(data).data
    assert expected_data['text'] == response.data[0]['text']
    assert expected_data['reply_for'] == response.data[0]['reply_for']

# use parametrize
# def test_get_wrong_fields(testuser, client, comment_with_post, url):
#     client.force_authenticate(testuser)
#     response = client.get(url)
#     data = {
#         'text': comment_with_post.text,
#         'reply_for': None,
#     }
#     assert 200 == response.status_code
#     expected_data = CommentsSerializer(data).data
#     assert expected_data['text'] == response.data[0]['text']
#     assert expected_data['reply_for'] == response.data[0]['reply_for']
