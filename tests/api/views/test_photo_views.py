from django.test import TestCase

from core import models
from tests.factories import models_factories


class TestPhotoListView(TestCase):
    def setUp(self, **kwargs):
        self.url = '/api/photos/'

    def test_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 405

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


class TestPhotoDetailView(TestCase):
    def setUp(self, **kwargs):
        self.base_url = '/api/photos'
        self.photo = models_factories.PhotoFactory()

    def test_get(self):
        response = self.client.get('{}/{}/'.format(self.base_url, self.photo.id))
        assert response.status_code == 404

    def test_patch(self):
        response = self.client.patch('{}/{}/'.format(self.base_url, self.photo.id), {},
                                     content_type='application/json')
        assert response.status_code == 404

    def test_put(self):
        response = self.client.put('{}/{}/'.format(self.base_url, self.photo.id), {},
                                   content_type='application/json')
        assert response.status_code == 404
