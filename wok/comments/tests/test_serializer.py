import pytest



def test_create_comment(client, _user):
    data = {
        'author': '_user',
        'post_id': '1',
        'reply_for_id': '',
        'text': "test_text"
    }
    response = client.post("api//v1/post/1/comment/", data)
    return_data = response.data

    assert data['author'] == return_data['author']
