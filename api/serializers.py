from rest_framework import serializers

from core import models as db_models

# TODO consider serpy to speed up the serialization:
# https://github.com/clarkduvall/serpy


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Location
        fields = '__all__'
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }


class ProducerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Producer
        fields = '__all__'
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'winery_location': {'lookup_field': 'uuid'},
        }


class ProducerSerializerDetailed(ProducerSerializer):
    winery_location_details = LocationSerializer(read_only=True, source='winery_location')


class BottleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Bottle
        fields = '__all__'  # Or: exclude = ('year',)
        read_only_fields = ('uuid',)
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'producer': {'lookup_field': 'uuid'},
            'vineyard_location': {'lookup_field': 'uuid'},
        }


class BottleSerializerDetailed(BottleSerializer):
    producer_details = ProducerSerializerDetailed(read_only=True, source='producer')
    vineyard_location_details = LocationSerializer(read_only=True, source='vineyard_location')
