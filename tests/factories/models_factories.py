"""
Factories are managed with FactoryBoy, see:
https://factoryboy.readthedocs.io/en/latest/index.html

Which include Fake, see:
https://faker.readthedocs.io/en/stable/index.html
"""
import linecache
import os
import random
from collections import namedtuple

import factory

from core import models


_ITALIAN_WINES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'italian_wines.txt')


def _count_italian_wines_file_lines():
    return 522
_ITALIAN_WINES_FILE_LINES_COUNT = _count_italian_wines_file_lines()


def _pick_random_wine():
    line_number = random.randint(1, _ITALIAN_WINES_FILE_LINES_COUNT)
    line = linecache.getline(_ITALIAN_WINES_FILE, line_number)
    name, label, region = line.split(';')
    name = name + ' ' + label
    Wine = namedtuple('Wine', 'name, region')
    return Wine(name=name, region=region)


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Location

    name = factory.Faker('city', locale='it_IT')


class ProducerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Producer

    name = factory.Faker('company', locale='it_IT')
    winery_location = factory.SubFactory(LocationFactory)


class BottleFactory:
    """
    A wrapper around the actual factory, to pick a random wine from a file first.
    Note that using a LazyAttribute would do the trick, but not with SubFactory (vineyard_location).
    """
    def __new__(self, do_add_photo=False, *args, **kwargs):
        random_wine = _pick_random_wine()
        if not kwargs.get('name'):
            kwargs['name'] = random_wine.name
        if not kwargs.get('vineyard_location'):
            kwargs['vineyard_location'] = LocationFactory(name=random_wine.region)
        obj = _BottleFactory(*args, **kwargs)
        if do_add_photo:
            PhotoFactory(bottle=obj)
        return obj


class _BottleFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('last_name', locale='it_IT')
    year = random.randint(1900, 2018)
    alcohol = random.choice(('12.0', '12.5', '13.0', '13.5', '14.0'))
    vineyard_location = factory.SubFactory(LocationFactory)
    producer = factory.SubFactory(ProducerFactory)

    class Meta:
        model = models.Bottle


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Photo

    bottle = factory.SubFactory(_BottleFactory)
    file = factory.Faker('file_path', locale='it_IT')
