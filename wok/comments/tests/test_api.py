import pytest
from model_bakery import baker

from comments.models import Comments
from comments.serializers import CommentsSerializer
from posts.models import Post

pytestmark = pytest.mark.django_db


def test_get_unauth(client, comment_with_post, url):
    response = client.get(url)
    assert 401 == response.status_code


def test_get_auth(auth, client, comment_with_post, url):
    response = client.get(url)
    data = {
        'text': comment_with_post.text,
        'reply_for': None,
    }
    assert 200 == response.status_code
    expected_data = CommentsSerializer(data).data
    assert expected_data['text'] == response.data[0]['text']
    assert expected_data['reply_for'] == response.data[0]['reply_for']


def test_get_comments_list(auth, client, post, url):
    baker.make(Comments, post=post, _quantity=3)
    response = client.get(url)
    assert 3 == len(response.data)



def test_post_unauth(post, url, client):
    response = client.post(url)
    assert 401 == response.status_code


def test_post_auth(post, url, client, auth):
    data = {
        'text': 'Тестовый',
        'reply_for': '',
    }
    response = client.post(url, data)
    assert 201 == response.status_code
    assert data['text'] == response.data['text']
    assert response.data['reply_for'] is None


def test_post_wrong_fields(auth, client, url):
    data = {
        'text': 12415,
        'reply_for': 6,
    }
    response = client.post(url, data)
    assert 400 == response.status_code

def test_post_empty(auth, client, url):
    data = {}
    response = client.post(url, data)
    assert 400 == response.status_code

