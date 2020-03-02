import pytest
from user.models import User
from storage.models import Storage

# @pytest.mark.django_db
def test_user_create(user):
    assert user.username == "test"
    user_all = User.objects.all()
    print(Storage.objects.all())
    print(user_all)

@pytest.mark.django_db
def test_user():
    user_all = User.objects.all()
    print(user_all)