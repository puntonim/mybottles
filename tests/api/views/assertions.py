import pytz

from django.conf import settings


def assertBottleEqual(serialized, bottle_instance):
    assert serialized['uuid'] == str(bottle_instance.uuid)
    assert serialized['name'] == bottle_instance.name
    assert serialized['alcohol'] == bottle_instance.alcohol
    assert serialized['year'] == bottle_instance.year
    creation_ts = bottle_instance.creation_ts.astimezone(pytz.timezone(settings.TIME_ZONE))
    assert serialized['creation_ts'] == creation_ts.isoformat()
    update_ts = bottle_instance.update_ts.astimezone(pytz.timezone(settings.TIME_ZONE))
    assert serialized['update_ts'] == update_ts.isoformat()
    assert serialized['url'] == 'http://testserver/api/bottles/{}/'.format(bottle_instance.uuid)
    assert serialized['producer'] == 'http://testserver/api/producers/{}/'.format(bottle_instance.producer.uuid)
    assert serialized['vineyard_location'] == 'http://testserver/api/locations/{}/'.format(bottle_instance.vineyard_location.uuid)
