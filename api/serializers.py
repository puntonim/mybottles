from rest_framework import serializers

from core import models as db_models

# TODO consider serpy to speed up the serialization:
# https://github.com/clarkduvall/serpy


class BottleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Bottle
        fields = '__all__'  # Or: exclude = ('slug',)
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'producer': {'lookup_field': 'uuid'},
            'vineyard_location': {'lookup_field': 'uuid'},
        }


class ProducerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Producer
        fields = '__all__'
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'winery_location': {'lookup_field': 'uuid'},
        }


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Location
        fields = '__all__'
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }
