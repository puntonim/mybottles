from django.test import TestCase

from core import models
from tests.factories import models_factories

from . import assertions


class TestPurchaseListView(TestCase):
    def setUp(self, **kwargs):
        self.url = '/api/purchases/'
        self.bottle = models_factories.BottleFactory()
        self.store = models_factories.StoreFactory()

    def test_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 405

    def test_post_required_fields_only(self):
        data = dict(
            bottle='http://testserver/api/bottles/{}/'.format(self.bottle.uuid),
            store='http://testserver/api/stores/{}/'.format(self.store.uuid),
        )
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert models.Purchase.objects.count() == 1
        purchase = models.Purchase.objects.order_by('-id')[0]
        assertions.assert_purchase_equal(response.json(), purchase)

    def test_post_full(self):
        data = dict(
            quantity=3,
            price_paid='12.50',
            price_original='15.80',
            date='2019-05-18',
            bottle='http://testserver/api/bottles/{}/'.format(self.bottle.uuid),
            store='http://testserver/api/stores/{}/'.format(self.store.uuid),
            is_gift=False,
            notes='This is my note',
        )
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert models.Purchase.objects.count() == 1
        purchase = models.Purchase.objects.order_by('-id')[0]
        assertions.assert_bottle_equal(response.json(), data, do_ignore_missing_in_instance_or_dict=True)
        assertions.assert_purchase_equal(response.json(), purchase)

    def test_validation(self):
        data = dict(
            quantity=3,
            bottle='http://testserver/api/bottles/{}/'.format(self.bottle.uuid),
            store='http://testserver/api/stores/{}/'.format(self.store.uuid),
            is_gift=True,
        )
        response = self.client.post(self.url, data)
        assert response.status_code == 400
        assert 'store' in response.json()
        del data['store']
        data['is_gift'] = False
        response = self.client.post(self.url, data)
        assert response.status_code == 400
        assert 'store' in response.json()
        data['is_gift'] = True
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert models.Purchase.objects.count() == 1
        purchase = models.Purchase.objects.order_by('-id')[0]
        assertions.assert_bottle_equal(response.json(), data, do_ignore_missing_in_instance_or_dict=True)
        assertions.assert_purchase_equal(response.json(), purchase)


class TestPurchaseDetailView(TestCase):
    def setUp(self, **kwargs):
        self.base_url = '/api/purchases'
        self.bottle = models_factories.BottleFactory(do_add_purchase=True)
        self.purchase = self.bottle.purchase_set.all().first()

    def test_get(self):
        response = self.client.get('{}/{}/'.format(self.base_url, self.purchase.uuid))
        assert response.status_code == 200
        purchase = models.Purchase.objects.get(uuid=self.purchase.uuid)
        assertions.assert_purchase_equal(response.json(), purchase)

    def test_patch(self):
        quantity = 123
        data = dict(quantity=quantity)
        response = self.client.patch('{}/{}/'.format(self.base_url, self.purchase.uuid), data,
                                     content_type='application/json')
        assert response.status_code == 200
        purchase = models.Purchase.objects.get(uuid=self.purchase.uuid)
        assert purchase.quantity == quantity
        assertions.assert_purchase_equal(response.json(), purchase)

    def test_put(self):
        quantity = 123
        bottle = models_factories.BottleFactory()
        store = models_factories.StoreFactory()
        data = dict(
            quantity=quantity,
            bottle='http://testserver/api/bottles/{}/'.format(bottle.uuid),
            store='http://testserver/api/stores/{}/'.format(store.uuid),
        )
        response = self.client.put('{}/{}/'.format(self.base_url, self.purchase.uuid), data,
                                   content_type='application/json')
        assert response.status_code == 200
        purchase = models.Purchase.objects.get(uuid=self.purchase.uuid)
        assert purchase.quantity == quantity
        assertions.assert_purchase_equal(response.json(), purchase)

    def test_validation(self):
        data = dict(
            is_gift=True,
        )
        response = self.client.patch('{}/{}/'.format(self.base_url, self.purchase.uuid), data,
                                     content_type='application/json')
        assert response.status_code == 400
        assert 'store' in response.json()
        data['store'] = None
        data['is_gift'] = False
        response = self.client.patch('{}/{}/'.format(self.base_url, self.purchase.uuid), data,
                                     content_type='application/json')
        assert response.status_code == 400
        assert 'store' in response.json()
        data['is_gift'] = False
        store = models_factories.StoreFactory()
        data['store'] = 'http://testserver/api/stores/{}/'.format(store.uuid)
        response = self.client.patch('{}/{}/'.format(self.base_url, self.purchase.uuid), data,
                                     content_type='application/json')
        assert response.status_code == 200
        purchase = models.Purchase.objects.get(uuid=self.purchase.uuid)
        assertions.assert_purchase_equal(response.json(), purchase)
