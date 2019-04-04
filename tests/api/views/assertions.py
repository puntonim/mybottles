import pytz

from django.conf import settings
from django.test import TestCase


def assertBottleEqual(serialized, bottle_instance):
    t = TestCase()
    t.assertEqual(serialized['uuid'], str(bottle_instance.uuid))
    t.assertEqual(serialized['name'], bottle_instance.name)
    t.assertEqual(serialized['alcohol'], bottle_instance.alcohol)
    t.assertEqual(serialized['year'], bottle_instance.year)
    creation_ts = bottle_instance.creation_ts.astimezone(pytz.timezone(settings.TIME_ZONE))
    t.assertEqual(serialized['creation_ts'], creation_ts.isoformat())
    update_ts = bottle_instance.update_ts.astimezone(pytz.timezone(settings.TIME_ZONE))
    t.assertEqual(serialized['update_ts'], update_ts.isoformat())
    t.assertEqual(serialized['url'], 'http://testserver/api/bottles/{}/'.format(bottle_instance.uuid))
    t.assertEqual(serialized['producer'], 'http://testserver/api/producers/{}/'.format(bottle_instance.producer.uuid))
    t.assertEqual(serialized['vineyard_location'], 'http://testserver/api/locations/{}/'.format(bottle_instance.vineyard_location.uuid))
