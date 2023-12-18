import pytest


class CreateCommentAPIView:
    url: str = "/api/v1/post/1/comment"

    def test_get_unauth(self, client, comment):
        response = client.get(self.URL)
        print(comment)
        assert comment == response.data
