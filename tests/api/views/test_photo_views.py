from django.test import TestCase

from core import models
from tests.factories import models_factories


class TestPhotoListView(TestCase):
    def setUp(self, **kwargs):
        self.url = '/api/photos/'

    def test_post(self):
        bottle = models_factories.BottleFactory()
        with open(__file__) as fopen:
            data = dict(
                bottle='http://testserver/api/bottles/{}/'.format(bottle.uuid),
                file=fopen,
            )
            response = self.client.post(self.url, data=data)
        assert response.status_code == 201
        assert models.Photo.objects.count() == 1
        photo = models.Photo.objects.all()[0]
        assert photo.bottle == bottle
        assert photo.file
        photo.file.delete()
