from storage.models import Storage


def test_storage_rest_api(c):
    r = c.get('/api/storage/')
    print(r.json())