from storage.models import Storage, Membership, Identifier
from pprint import pprint
import pytest
from user.models import User
from storage.utils import create_storage


@pytest.fixture
def storage(user):
    return Membership.objects.get(user=user, storage__is_personal_storage=True).storage


@pytest.fixture
def new_storage(user):
    return create_storage(user, '新建存储库')


class TestStorageManage:
    def test_get_all_storage(self, c, storage):
        r = c.get('/api/storage/')
        pprint(r.json())
        res = r.json()
        assert len(res) > 0
        assert res[0]['storage_id'] == storage.id

    def test_storage_detail(self, c):
        res = c.get('/api/storage/').json()
        storage_id = res[0]['storage_id']
        r = c.get(f'/api/storage/{storage_id}/')
        print(r.json())
        assert (r.json()['name'] == '文件')

    def test_create(self, c):
        # default content_type is multipart/form-data
        r = c.post('/api/storage/', {'name': '测试群'})
        assert r.status_code == 200
        assert r.json()['storage_id']

    def test_modify_name(self, c, new_storage):
        r = c.put(f'/api/storage/{new_storage.id}/', {'name': '新名字'})
        assert r.status_code == 200
        r = c.get(f'/api/storage/{new_storage.id}/')
        assert (r.json()['name'] == '新名字')

    def test_modify_name_with_invalid_data(self, c, new_storage):
        r = c.put(f'/api/storage/{new_storage.id}/', {'nme': '新名字'})
        assert r.status_code == 400

    def test_delete(self, c, new_storage):
        r = c.delete(f'/api/storage/{new_storage.id}/')
        assert r.status_code == 200
        res = c.get('/api/storage/').json()
        assert new_storage.id not in [i['storage_id'] for i in res]


@pytest.fixture
def api_base(storage):
    return f'/api/storage/{storage.id}/'


@pytest.fixture
def api_url(storage, api_base):
    return f'{api_base}{storage.root_identifier.id}/'


@pytest.fixture
def new_folder(storage):
    return Identifier.objects.create(name="new_folder", parent=storage.root_identifier, owner=storage.users.get())


@pytest.fixture
def new_folder2(storage):
    return Identifier.objects.create(name="new_folder2", parent=storage.root_identifier, owner=storage.users.get())


class TestStorageContentManage:
    def test_get_folder_content(self, c, new_folder, api_url):
        r = c.get(api_url)
        print(r.json())
        assert r.json()['content'][0]['name'] == 'new_folder'

    def test_create_folder(self, c, api_url):
        r = c.post(api_url, {'name': 'new_folder'})
        assert r.status_code == 200
        assert r.json()['name'] == 'new_folder'

    def test_delete_folder(self, c, new_folder, api_base, api_url):
        r = c.delete(api_url, {"id": [new_folder.id]})
        assert r.status_code == 200
        r = c.get(api_url)
        print(r.json())
        assert r.json()['content'] == []

    def test_modify_folder(self, c, new_folder, api_base, api_url):
        r = c.put(f'{api_base}{new_folder.id}/', {'name': 'name_changed'})
        assert r.status_code == 200
        r = c.get(api_url)
        assert r.json()['content'][0]['name'] == 'name_changed'

    @pytest.mark.parametrize("action", ('move', 'copy'))
    def test_copy_folder(self, c, new_folder, new_folder2, api_url, storage, api_base, action):
        r = c.put(f'{api_url}{action}/',
                  {'source_id': [new_folder.id],
                   'destination_storage_id': storage.id,
                   'destination_directory_id': new_folder2.id})
        assert r.status_code == 200
        r = c.get(f'{api_base}{new_folder2.id}/')
        assert len(r.json()['content']) == 1
        r = c.get(api_url)
        if action == 'move':
            assert len(r.json()['content']) == 1
        else:
            assert len(r.json()['content']) == 2


def test_permission(client):
    user1 = User.objects.create(username="user1", nickname="test_nickname1",
                                password='test')
    user2 = User.objects.create(username="user2", nickname="test_nickname2",
                                password='test')
    user1_storage_id = Storage.objects.get(users=user1).id
    client.login(username='user2', password='test')
    r = client.get(f'/api/storage/{user1_storage_id}/')
    assert r.status_code == 403
