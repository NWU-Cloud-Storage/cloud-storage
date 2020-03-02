import pytest
from user.models import User

@pytest.fixture(scope='function')
def user(db):
    user = User.objects.create(username="test", nickname="test_nickname",
                               password=User.objects.make_random_password())
    return user