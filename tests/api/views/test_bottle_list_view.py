from django.test import TestCase

from tests.factories import models_factories

from . import assertions


class TestBottleListView(TestCase):
    def setUp(self, **kwargs):
        self.url = '/api/bottles/'
        self.bottle1 = models_factories.BottleFactory()
        self.bottle2 = models_factories.BottleFactory()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
        assertions.assertBottleEqual(response.json()['results'][0], self.bottle2)
        assertions.assertBottleEqual(response.json()['results'][1], self.bottle1)
