from django.test import TestCase

from core import models
from tests.factories import models_factories

from . import assertions


class TestLocationListView(TestCase):
    def setUp(self, **kwargs):
        self.url = '/api/locations/'
        self.location1 = models_factories.LocationFactory()
        self.location2 = models_factories.LocationFactory()

    def test_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.json()['count'] == 2
        assertions.assert_location_equal(response.json()['results'][0], self.location2)
        assertions.assert_location_equal(response.json()['results'][1], self.location1)

    def test_post(self):
        data = {'name': 'new location'}
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert models.Location.objects.count() == 3
        location = models.Location.objects.order_by('-id')[0]
        assertions.assert_location_equal(response.json(), location)


class TestLocationDetailView(TestCase):
    def setUp(self, **kwargs):
        self.base_url = '/api/locations'
        self.location = models_factories.LocationFactory()

    def test_get(self):
        location = models.Location.objects.all()[0]
        response = self.client.get('{}/{}/'.format(self.base_url, location.uuid))
        assert response.status_code == 200
        assertions.assert_location_equal(response.json(), location)

    def test_patch(self):
        name = 'newname'
        data = dict(name=name)
        response = self.client.patch('{}/{}/'.format(self.base_url, self.location.uuid), data,
                                     content_type='application/json')
        assert response.status_code == 200
        location = models.Location.objects.get(uuid=self.location.uuid)
        assert location.name == name
        assertions.assert_location_equal(response.json(), location)

    def test_put(self):
        name = 'newname'
        data = dict(name=name)
        response = self.client.put('{}/{}/'.format(self.base_url, self.location.uuid), data,
                                   content_type='application/json')
        assert response.status_code == 200
        location = models.Location.objects.get(uuid=self.location.uuid)
        assert location.name == name
        assertions.assert_location_equal(response.json(), location)
