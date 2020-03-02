from user.models import User
from storage.models import Storage

# @pytest.mark.django_db
def test_user_create(user):
    assert user.username == "test"
    user_all = User.objects.all()
    print(Storage.objects.all())
    print(user_all)


def test_user_rest_api(c, user):
    username = user.username

    # 获取某用户资料
    response = c.get('/api/user/' + username + '/')
    assert response.status_code == 200
    print(response.json())
    assert username in response.json()['username']

    # 获取个人全部资料
    response = c.get('/api/user/')
    assert username in response.json()['username']
    assert user.nickname in response.json()['nickname']

