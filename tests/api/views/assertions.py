from types import SimpleNamespace

import pytz
from django.conf import settings


class _ModelAssertionBase:
    def __init__(self, serialized, instance_or_dict):
        self.serialized = serialized
        # If `instance_or_dict` is a dict then change it to a SimpleNamespace to
        # enable the dot notation.
        self.object = instance_or_dict
        if isinstance(self.object, dict):
            self.object = SimpleNamespace(**self.object)

    def assert_equal(self, base_url=None, do_ignore_missing_in_instance_or_dict=False):
        self.base_url = base_url
        for attr in self._get_all_attrs():
            if not hasattr(self.object, attr):
                if do_ignore_missing_in_instance_or_dict:
                    continue
            else:
                if not getattr(self.object, attr):
                    assert not self.serialized[attr]
                    continue

            if hasattr(self, '_assert_attr_{}'.format(attr)):
                getattr(self, '_assert_attr_{}'.format(attr))()
            else:
                self._assert_default_attr(attr)

    def _get_all_attrs(self):
        attrs = list(self.serialized.keys())
        for attr in self.object.__dict__.keys():
            if attr.startswith('_'):
                continue
            if attr.endswith('_id'):
                attrs.append(attr[:-3])
        return attrs

    def _assert_default_attr(self, attr):
        obj_val = getattr(self.object, attr)
        if isinstance(self.serialized[attr], str):
            obj_val = str(obj_val)
        assert self.serialized[attr] == obj_val

    def _assert_attr_creation_ts(self):
        creation_ts = self.object.creation_ts.astimezone(pytz.timezone(settings.TIME_ZONE))
        assert self.serialized['creation_ts'] == creation_ts.isoformat()

    def _assert_attr_update_ts(self):
        update_ts = self.object.update_ts.astimezone(pytz.timezone(settings.TIME_ZONE))
        assert self.serialized['update_ts'] == update_ts.isoformat()

    def _assert_attr_url(self):
        if hasattr(self.object, 'uuid'):
            assert self.serialized['url'] == '{}/{}/'.format(self.base_url, self.object.uuid)

    def _assert_attr_producer(self):
        if isinstance(self.object.producer, str):
            producer_uuid = self.object.producer.split('/')[-2]
        else:
            producer_uuid = self.object.producer.uuid
        assert self.serialized['producer'] == 'http://testserver/api/producers/{}/'.format(producer_uuid)

    def _assert_attr_bottle(self):
        if isinstance(self.object.bottle, str):
            bottle_uuid = self.object.bottle.split('/')[-2]
        else:
            bottle_uuid = self.object.bottle.uuid
        assert self.serialized['bottle'] == 'http://testserver/api/bottles/{}/'.format(bottle_uuid)

    def _assert_attr_store(self):
        if isinstance(self.object.store, str):
            store_uuid = self.object.store.split('/')[-2]
        else:
            store_uuid = self.object.store.uuid
        assert self.serialized['store'] == 'http://testserver/api/stores/{}/'.format(store_uuid)

    def _assert_attr_producer_details(self):
        assert_producer_equal(self.serialized['producer_details'], self.object.producer)

    def _assert_attr_vineyard_location(self):
        if isinstance(self.object.vineyard_location, str):
            vineyard_location_uuid = self.object.vineyard_location.split('/')[-2]
        else:
            vineyard_location_uuid = self.object.vineyard_location.uuid
        assert self.serialized['vineyard_location'] == 'http://testserver/api/locations/{}/'.format(
            vineyard_location_uuid)

    def _assert_attr_vineyard_location_details(self):
        assert_location_equal(self.serialized['vineyard_location_details'], self.object.vineyard_location)

    def _assert_attr_winery_location(self):
        if isinstance(self.object.winery_location, str):
            winery_location_uuid = self.object.winery_location.split('/')[-2]
        else:
            winery_location_uuid = self.object.winery_location.uuid
        assert self.serialized['winery_location'] == 'http://testserver/api/locations/{}/'.format(winery_location_uuid)

    def _assert_attr_winery_location_details(self):
        assert_location_equal(self.serialized['winery_location_details'], self.object.winery_location)

    def _assert_attr_store_details(self):
        assert_store_equal(self.serialized['store_details'], self.object.store)

    def _assert_attr_photos(self):
        assert len(self.serialized['photos']) == self.object.photo_set.count()
        for photo in self.object.photo_set.all():
            assert photo.file.url in self.serialized['photos']

    def _assert_attr_purchases(self):
        assert len(self.serialized['purchases']) == self.object.purchase_set.count()
        for purchase in self.object.purchase_set.all():
            assert 'http://testserver/api/purchases/{}/'.format(purchase.uuid) in self.serialized['purchases']


def assert_bottle_equal(serialized, instance_or_dict, do_ignore_missing_in_instance_or_dict=False):
    model_assertion = _ModelAssertionBase(serialized, instance_or_dict)
    model_assertion.assert_equal(base_url='http://testserver/api/bottles',
                                 do_ignore_missing_in_instance_or_dict=do_ignore_missing_in_instance_or_dict)


def assert_producer_equal(serialized, instance_or_dict, do_ignore_missing_in_instance_or_dict=False):
    model_assertion = _ModelAssertionBase(serialized, instance_or_dict)
    model_assertion.assert_equal(base_url='http://testserver/api/producers',
                                 do_ignore_missing_in_instance_or_dict=do_ignore_missing_in_instance_or_dict)


def assert_location_equal(serialized, instance_or_dict, do_ignore_missing_in_instance_or_dict=False):
    model_assertion = _ModelAssertionBase(serialized, instance_or_dict)
    model_assertion.assert_equal(base_url='http://testserver/api/locations',
                                 do_ignore_missing_in_instance_or_dict=do_ignore_missing_in_instance_or_dict)


def assert_store_equal(serialized, instance_or_dict, do_ignore_missing_in_instance_or_dict=False):
    model_assertion = _ModelAssertionBase(serialized, instance_or_dict)
    model_assertion.assert_equal(base_url='http://testserver/api/stores',
                                 do_ignore_missing_in_instance_or_dict=do_ignore_missing_in_instance_or_dict)


def assert_purchase_equal(serialized, instance_or_dict, do_ignore_missing_in_instance_or_dict=False):
    model_assertion = _ModelAssertionBase(serialized, instance_or_dict)
    model_assertion.assert_equal(base_url='http://testserver/api/purchases',
                                 do_ignore_missing_in_instance_or_dict=do_ignore_missing_in_instance_or_dict)
