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
