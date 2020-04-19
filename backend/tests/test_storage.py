from storage.models import Storage
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


def test_storage_rest_api(c):
    r = c.get('/api/storage/')
    res = r.json()

    storage_id = res[0]['storage_id']
    root_folder_id = res[0]['root_folder_id']

    r = c.post(f'/api/storage/{storage_id}/',
               {'name': 'new_folder'}, content_type='application/json')
    assert r.status_code == 200
    assert r.json()['name'] == 'new_folder'
    folder_id = r.json()['id']

    r = c.put(f'/api/storage/{storage_id}/{folder_id}/',
              {'name': 'name_changed'}, content_type='application/json')
    assert r.status_code == 200

    r = c.get(f'/api/storage/{storage_id}/')
    content = r.json()['content']
    assert content[0]['name'] == 'name_changed'

    r = c.put(f'/api/storage/{storage_id}/copy/',
              {'source_id': [folder_id],
               'destination_storage_id': storage_id,
               'destination_directory_id': root_folder_id},
              content_type='application/json')
    assert r.status_code == 200

    r = c.get(f'/api/storage/{storage_id}/')
    pprint(r.json())

    r = c.delete(f'/api/storage/{storage_id}/', {'id': [folder_id]}, content_type='application/json')
    assert r.status_code == 200


def test_permission(client):
    user1 = User.objects.create(username="user1", nickname="test_nickname1",
                                password='test')
    user2 = User.objects.create(username="user2", nickname="test_nickname2",
                                password='test')
    user1_storage_id = Storage.objects.get(users=user1).id
    client.login(username='user2', password='test')
    r = client.get(f'/api/storage/{user1_storage_id}/')
    assert r.status_code == 403
