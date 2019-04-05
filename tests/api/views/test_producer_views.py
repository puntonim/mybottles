from django.test import TestCase

from core import models
from tests.factories import models_factories

from . import assertions


class TestProducerDetailView(TestCase):
    def setUp(self, **kwargs):
        self.base_url = '/api/producers'
        self.producer = models_factories.ProducerFactory()

    def test_get(self):
        producer = models.Producer.objects.all()[0]
        response = self.client.get('{}/{}/'.format(self.base_url, producer.uuid))
        assert response.status_code == 200
        assertions.assert_producer_equal(response.json(), producer)

    def test_patch(self):
        winery_location = models_factories.LocationFactory()
        data = dict(winery_location=winery_location.get_absolute_url())
        response = self.client.patch('{}/{}/'.format(self.base_url, self.producer.uuid), data, content_type='application/json')
        assert response.status_code == 200
        producer = models.Producer.objects.get(uuid=self.producer.uuid)
        assert producer.winery_location == winery_location
        assertions.assert_producer_equal(response.json(), producer)

    def test_put(self):
        name = 'newname'
        winery_location = models_factories.LocationFactory()
        data = dict(name=name, winery_location=winery_location.get_absolute_url())
        response = self.client.put('{}/{}/'.format(self.base_url, self.producer.uuid), data, content_type='application/json')
        assert response.status_code == 200
        producer = models.Producer.objects.get(uuid=self.producer.uuid)
        assert producer.name == name
        assert producer.winery_location == winery_location
        assertions.assert_producer_equal(response.json(), producer)
