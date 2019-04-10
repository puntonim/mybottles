import pytest
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.test import TestCase

from core.models import Purchase
from tests.factories import models_factories


class TestPurchaseModel(TestCase):
    def setUp(self):
        self.bottle = models_factories.BottleFactory()
        self.store = models_factories.StoreFactory()

    def test_validation_in_create(self):
        purchase = Purchase.objects.create(
            bottle=self.bottle,
            quantity=3,
            store=self.store,
        )
        assert purchase

    def test_validation_in_create_exception(self):
        with pytest.raises(ValidationError):
            Purchase.objects.create(
                bottle=self.bottle,
                quantity=3,
                store=self.store,
                is_gift=True
            )

    def test_validation_in_save_new_obj(self):
        purchase = Purchase(
            bottle=self.bottle,
            quantity=3,
            is_gift=False,
        )
        with pytest.raises(ValidationError):
            purchase.save()
        purchase.is_gift = True
        purchase.store = self.store
        with pytest.raises(ValidationError):
            purchase.save()
        purchase.is_gift = False
        purchase.save()
        assert purchase

    def test_validation_in_save_edit_obj(self):
        purchase = Purchase.objects.create(
            bottle=self.bottle,
            quantity=3,
            store=self.store,
        )

        purchase.is_gift = True
        with pytest.raises(ValidationError):
            purchase.save()
        purchase.is_gift = False
        purchase.store = None
        with pytest.raises(ValidationError):
            purchase.save()
        purchase.is_gift = True
        purchase.save()
        assert purchase

    def test_validation_in_model_forms(self):
        data = dict(
            bottle=self.bottle.id,
            quantity=3,
            is_gift=False,
        )
        form = PurchaseForm(data)
        assert not form.is_valid()

        data['is_gift'] = True
        data['store'] = self.store.id
        assert not PurchaseForm(data).is_valid()
        data['is_gift'] = False
        form = PurchaseForm(data)
        assert form.is_valid()
        purchase = form.save()
        assert purchase


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['bottle', 'quantity', 'store', 'is_gift']
