from django.test import TestCase

from core import models
from tests.factories import models_factories

from . import assertions


class TestBottleListView(TestCase):
    def setUp(self, **kwargs):
        self.url = '/api/bottles/'
        self.bottle1 = models_factories.BottleFactory(do_add_photo=True)
        self.bottle2 = models_factories.BottleFactory(do_add_photo=True)

    def test_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.json()['count'] == 2
        assertions.assert_bottle_equal(response.json()['results'][0], self.bottle2)
        assertions.assert_bottle_equal(response.json()['results'][1], self.bottle1)

    def test_post_name_only(self):
        data = {'name': 'new wine'}
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert models.Bottle.objects.count() == 3
        bottle = models.Bottle.objects.order_by('-update_ts')[0]
        assertions.assert_bottle_equal(response.json(), bottle)

    def test_post_full(self):
        producer = models_factories.ProducerFactory()
        location = models_factories.LocationFactory()
        data = dict(
            name='new wine',
            producer='http://testserver/api/producers/{}/'.format(producer.uuid),
            vineyard_location='http://testserver/api/locations/{}/'.format(location.uuid),
            year=2010,
            alcohol='12.5',
        )
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert models.Bottle.objects.count() == 3
        bottle = models.Bottle.objects.order_by('-update_ts')[0]
        assertions.assert_bottle_equal(response.json(), data, do_ignore_missing_in_instance_or_dict=True)
        assertions.assert_bottle_equal(response.json(), bottle)


class TestBottleDetailView(TestCase):
    def setUp(self, **kwargs):
        self.base_url = '/api/bottles'
        self.bottle = models_factories.BottleFactory(name='initialname', year=2019, do_add_photo=True)

    def test_get(self):
        response = self.client.get('{}/{}/'.format(self.base_url, self.bottle.uuid))
        assert response.status_code == 200
        bottle = models.Bottle.objects.get(uuid=self.bottle.uuid)
        assertions.assert_bottle_equal(response.json(), bottle)

    def test_patch(self):
        year = 2010
        data = dict(year=year)
        response = self.client.patch('{}/{}/'.format(self.base_url, self.bottle.uuid), data,
                                     content_type='application/json')
        assert response.status_code == 200
        bottle = models.Bottle.objects.get(uuid=self.bottle.uuid)
        assert bottle.year == year
        assertions.assert_bottle_equal(response.json(), bottle)

    def test_put(self):
        name = 'newname'
        year = 2010
        data = dict(name=name, year=year)
        response = self.client.put('{}/{}/'.format(self.base_url, self.bottle.uuid), data,
                                   content_type='application/json')
        assert response.status_code == 200
        bottle = models.Bottle.objects.get(uuid=self.bottle.uuid)
        assert bottle.name == name
        assert bottle.year == year
        assertions.assert_bottle_equal(response.json(), bottle)
