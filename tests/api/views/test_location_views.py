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
