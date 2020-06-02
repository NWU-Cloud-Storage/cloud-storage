from storage.models import Storage, Membership, Identifier
from pprint import pprint
import pytest
from user.models import User


class TestStorageManage:
    def test_get_all_storage(self, c):
        r = c.get('/api/storage/')
        print(r.json())
        res = r.json()
        assert len(res) > 0

    def test_storage_detail(self, c):
        res = c.get('/api/storage/').json()
        storage_id = res[0]['storage_id']
        r = c.get(f'/api/storage/{storage_id}/')
        print(r.json())
        assert (r.json()['name'] == '文件')

    def test_create(self, c):
        # default content_type is multipart/form-data
        r = c.post('/api/storage/', {'name': '测试群'}, content_type='application/json')
        assert r.status_code == 200
        assert r.json()['storage_id']

    def test_modify_name(self, c):
        r = c.post('/api/storage/', {'name': '测试群'}, content_type='application/json')
        storage_id = r.json()['storage_id']
        r = c.put(f'/api/storage/{storage_id}/', {'name': '新名字'}, content_type='application/json')
        assert r.status_code == 200
        r = c.get(f'/api/storage/{storage_id}/')
        assert (r.json()['name'] == '新名字')

    def test_delete(self, c):
        r = c.post('/api/storage/', {'name': '测试群'}, content_type='application/json')
        storage_id = r.json()['storage_id']
        r = c.delete(f'/api/storage/{storage_id}/')
        assert r.status_code == 200
        res = c.get('/api/storage/').json()
        assert storage_id not in [i['storage_id'] for i in res]


@pytest.fixture
def storage(user):
    return Membership.objects.get(user=user, storage__is_personal_storage=True).storage


@pytest.fixture
def new_folder(storage):
    return Identifier.objects.create(name="new_folder", parent=storage.root_identifier)


class TestStorageContentManage:
    def __init__(self, storage):
        self.storage_id = storage.id
        self.root_folder_id = storage.root_identifier.id
        self.api_base = f'/api/storage/{self.storage_id}/'
        self.api_url = f'{self.api_base}{self.root_folder_id}/'

    def test_get_folder_content(self, c, new_folder):
        r = c.get(self.api_url)
        assert r.json()['content'][0]['name'] == 'new_folder'

    def test_create_folder(self, c):
        r = c.post(self.api_url, {'name': 'new_folder'}, content_type='application/json')
        assert r.status_code == 200
        assert r.json()['name'] == 'new_folder'

    def test_delete_folder(self, c, new_folder):
        r = c.delete(self.api_base, {"id": [new_folder.id]}, content_type='application/json')
        assert r.status_code == 200
        r = c.get(self.api_url)
        assert r.json()['content'] == []

    def test_modify_folder(self, c, new_folder):
        r = c.put(f'{self.api_base}{new_folder.id}/', {'name': 'name_changed'}, content_type='application/json')
        assert r.status_code == 200
        r = c.get(self.api_url)
        assert r.json()['content'][0]['name'] == 'name_changed'

    def test_copy_folder(self, c, new_folder):
        r = c.put(f'{self.api_base}copy/',
                  {'source_id': [new_folder.id],
                   'destination_storage_id': self.storage_id,
                   'destination_directory_id': self.root_folder_id},
                  content_type='application/json')
        assert r.status_code == 200
        r = c.get(self.api_url)
        assert len(r.json()['content']) == 2

    def test_move_folder(self, c, new_folder, storage):
        new_folder2 = Identifier.objects.create(name="new_folder2", parent=storage.root_identifier)
        r = c.put(f'{self.api_base}move/',
                  {'source_id': [new_folder.id],
                   'destination_storage_id': self.storage_id,
                   'destination_directory_id': new_folder2.id},
                  content_type='application/json')
        assert r.status_code == 200
        r = c.get(f'{self.api_base}{new_folder2.id}/')
        assert len(r.json()['content']) == 1


def test_permission(client):
    user1 = User.objects.create(username="user1", nickname="test_nickname1",
                                password='test')
    user2 = User.objects.create(username="user2", nickname="test_nickname2",
                                password='test')
    user1_storage_id = Storage.objects.get(users=user1).id
    client.login(username='user2', password='test')
    r = client.get(f'/api/storage/{user1_storage_id}/')
    assert r.status_code == 403
