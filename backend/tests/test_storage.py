from storage.models import Storage, Membership, Identifier
from pprint import pprint
import pytest
from user.models import User
from storage.utils import create_storage
from django.core.exceptions import ObjectDoesNotExist


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
        assert len(res) == 1
        assert res[0]['storage_id'] == storage.id

    def test_storage_detail(self, c):
        res = c.get('/api/storage/').json()
        storage_id = res[0]['storage_id']
        r = c.get(f'/api/storage/{storage_id}/')
        print(r.json())
        assert (r.json()['name'] == '文件')

    def test_create(self, c):
        r = c.post('/api/storage/', {'name': '测试群'})
        assert r.status_code == 200
        assert r.json()['storage_id']
        r = c.get('/api/storage/')
        assert len(r.json()) == 2

    def test_modify_name(self, c, new_storage):
        r = c.put(f'/api/storage/{new_storage.id}/', {'name': '新名字'})
        assert r.status_code == 200
        r = c.get(f'/api/storage/{new_storage.id}/')
        assert (r.json()['name'] == '新名字')

    def test_modify_name_with_invalid_data(self, c, new_storage):
        r = c.put(f'/api/storage/{new_storage.id}/', {'malformed_name': '新名字'})
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


@pytest.fixture
def user2():
    return User.objects.get(username="test2")


def test_permission(c, user2):
    user2_storage_id = Storage.objects.get(users=user2).id
    r = c.get(f'/api/storage/{user2_storage_id}/')
    assert r.status_code == 403


def test_get_permissions(c):
    r = c.get('/api/storage/permissions/')
    pprint(r.json())
    assert 'name' in r.json()[0]


class TestStorageMemberManage:
    def test_get_members(self, c, new_storage):
        r = c.get(f'/api/storage/{new_storage.id}/member/')
        assert r.json()[0] == {'nickname': 'test_nickname', 'permission': 'owner', 'username': 'test'}

    def test_add_member(self, c, new_storage, user2):
        r = c.put(f'/api/storage/{new_storage.id}/member/', {"username": user2.username})
        membership = Membership.objects.filter(storage=new_storage)
        assert len(membership) == 2

    def test_modify_permission(self, c, new_storage, user2):
        Membership.objects.create(user=user2, storage=new_storage)
        r = c.put(f'/api/storage/{new_storage.id}/member/{user2.username}/',
                  {"permission": "owner"})
        assert r.status_code == 200
        assert Membership.objects.get(user=user2, storage=new_storage).permission == 'owner'

    def test_delete_member(self, c, new_storage, user2):
        Membership.objects.create(user=user2, storage=new_storage)
        r = c.delete(f'/api/storage/{new_storage.id}/member/{user2.username}/')
        assert r.status_code == 200
        with pytest.raises(ObjectDoesNotExist):
            Membership.objects.get(user=user2, storage=new_storage)


