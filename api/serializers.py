from rest_framework import serializers

from core import models as db_models

# TODO consider serpy to speed up the serialization:
# https://github.com/clarkduvall/serpy


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Location
        fields = ('url', 'uuid', 'name')
        read_only_fields = ('uuid',)
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }


class ProducerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Producer
        fields = ('url', 'uuid', 'name', 'winery_location')
        read_only_fields = ('uuid',)
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'winery_location': {'lookup_field': 'uuid'},
        }


class ProducerSerializerDetailed(ProducerSerializer):
    winery_location_details = LocationSerializer(read_only=True, source='winery_location')

    class Meta(ProducerSerializer.Meta):
        fields = ProducerSerializer.Meta.fields + ('winery_location_details',)


class BottleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Bottle
        # fields = '__all__'  # Or: exclude = ('year',)  # But this was you cannot control the order.
        fields = ('url', 'uuid', 'update_ts', 'name', 'producer', 'vineyard_location', 'year', 'alcohol',)
        read_only_fields = ('uuid',)
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'producer': {'lookup_field': 'uuid'},
            'vineyard_location': {'lookup_field': 'uuid'},
        }


class BottleSerializerDetailed(BottleSerializer):
    producer_details = ProducerSerializerDetailed(read_only=True, source='producer')
    vineyard_location_details = LocationSerializer(read_only=True, source='vineyard_location')

    class Meta(BottleSerializer.Meta):
        fields = BottleSerializer.Meta.fields + ('producer_details', 'vineyard_location_details')
