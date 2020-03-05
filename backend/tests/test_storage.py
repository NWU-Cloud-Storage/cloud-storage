from storage.models import Storage


def test_storage_rest_api(c):
    r = c.get('/api/storage/')
    print(r.json())
    res = r.json()
    assert len(res) > 0

    storage_id = res[0]['storage_id']
    r = c.get(f'/api/storage/{storage_id}/')
    print(r.json())

    r = c.post(f'/api/storage/{storage_id}/', {'name': 'new_folder'})
    assert r.status_code == 200
    assert r.json()['name'] == 'new_folder'
    folder_id = r.json()['id']

    r = c.put(f'/api/storage/{storage_id}/{folder_id}/', {'name': 'name_changed'})
    assert r.status_code == 200