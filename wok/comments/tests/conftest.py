import pytest

from django.contrib.auth.models import User

from rest_framework.test import APIClient

@pytest.fixture()
def client():
    return APIClient()

@pytest.fixture()
def _user():
    user1 = User(username='user1')

    return user1