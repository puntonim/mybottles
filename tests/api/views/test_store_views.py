from django.test import TestCase

from core import models
from tests.factories import models_factories

from . import assertions


class TestStoreListView(TestCase):
    def setUp(self, **kwargs):
        self.url = '/api/stores/'
        self.store1 = models_factories.StoreFactory()
        self.store2 = models_factories.StoreFactory()

    def test_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.json()['count'] == 2
        assertions.assert_store_equal(response.json()['results'][0], self.store2)
        assertions.assert_store_equal(response.json()['results'][1], self.store1)

    def test_post(self):
        data = {'name': 'new store'}
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert models.Store.objects.count() == 3
        store = models.Store.objects.order_by('-id')[0]
        assertions.assert_store_equal(response.json(), store)


class TestStoreDetailView(TestCase):
    def setUp(self, **kwargs):
        self.base_url = '/api/stores'
        self.store = models_factories.StoreFactory(name='new store')

    def test_get(self):
        response = self.client.get('{}/{}/'.format(self.base_url, self.store.uuid))
        assert response.status_code == 200
        store = models.Store.objects.get(uuid=self.store.uuid)
        assertions.assert_store_equal(response.json(), store)

    def test_patch(self):
        name = 'newstore2'
        data = dict(name=name)
        response = self.client.patch('{}/{}/'.format(self.base_url, self.store.uuid), data,
                                     content_type='application/json')
        assert response.status_code == 200
        store = models.Store.objects.get(uuid=self.store.uuid)
        assert store.name == name
        assertions.assert_store_equal(response.json(), store)

    def test_put(self):
        name = 'newstore2'
        data = dict(name=name)
        response = self.client.put('{}/{}/'.format(self.base_url, self.store.uuid), data,
                                   content_type='application/json')
        assert response.status_code == 200
        store = models.Store.objects.get(uuid=self.store.uuid)
        assert store.name == name
        assertions.assert_store_equal(response.json(), store)
