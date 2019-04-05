from django.test import TestCase

from core import models
from tests.factories import models_factories

from . import assertions


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
        response = self.client.patch('{}/{}/'.format(self.base_url, self.location.uuid), data, content_type='application/json')
        assert response.status_code == 200
        location = models.Location.objects.get(uuid=self.location.uuid)
        assert location.name == name
        assertions.assert_location_equal(response.json(), location)

    def test_put(self):
        name = 'newname'
        data = dict(name=name)
        response = self.client.put('{}/{}/'.format(self.base_url, self.location.uuid), data, content_type='application/json')
        assert response.status_code == 200
        location = models.Location.objects.get(uuid=self.location.uuid)
        assert location.name == name
        assertions.assert_location_equal(response.json(), location)
