from django.test import TestCase

from core import models
from tests.factories import models_factories

from . import assertions


class TestProducerListView(TestCase):
    def setUp(self, **kwargs):
        self.url = '/api/producers/'
        self.producer1 = models_factories.ProducerFactory()
        self.producer2 = models_factories.ProducerFactory()

    def test_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.json()['count'] == 2
        assertions.assert_producer_equal(response.json()['results'][0], self.producer2)
        assertions.assert_producer_equal(response.json()['results'][1], self.producer1)

    def test_post_name_only(self):
        data = {'name': 'new producer'}
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert models.Producer.objects.count() == 3
        producer = models.Producer.objects.order_by('-id')[0]
        assertions.assert_producer_equal(response.json(), producer)

    def test_post_full(self):
        location = models_factories.LocationFactory()
        data = dict(
            name='new producer',
            vineyard_location='http://testserver/api/locations/{}/'.format(location.uuid),
        )
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert models.Producer.objects.count() == 3
        producer = models.Producer.objects.order_by('-id')[0]
        assertions.assert_producer_equal(response.json(), data, do_ignore_missing_in_instance_or_dict=True)
        assertions.assert_producer_equal(response.json(), producer)


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
        response = self.client.patch('{}/{}/'.format(self.base_url, self.producer.uuid), data,
                                     content_type='application/json')
        assert response.status_code == 200
        producer = models.Producer.objects.get(uuid=self.producer.uuid)
        assert producer.winery_location == winery_location
        assertions.assert_producer_equal(response.json(), producer)

    def test_put(self):
        name = 'newname'
        winery_location = models_factories.LocationFactory()
        data = dict(name=name, winery_location=winery_location.get_absolute_url())
        response = self.client.put('{}/{}/'.format(self.base_url, self.producer.uuid), data,
                                   content_type='application/json')
        assert response.status_code == 200
        producer = models.Producer.objects.get(uuid=self.producer.uuid)
        assert producer.name == name
        assert producer.winery_location == winery_location
        assertions.assert_producer_equal(response.json(), producer)
