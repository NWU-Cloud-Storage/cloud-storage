import pytest
from user.models import User

@pytest.fixture(scope='function')
def user(db):
    user = User.objects.create(username="test", nickname="test_nickname",
                               password='test')
    return user


@pytest.fixture(scope='function')
def c(client, user):
    client.login(username='test', password='test')
    return client