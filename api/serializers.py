from rest_framework import serializers

from core import models as db_models

# TODO consider serpy to speed up the serialization:
# https://github.com/clarkduvall/serpy


class BottleSerializer(serializers.HyperlinkedModelSerializer):
    """
    >>> BottleSerializer():
        url = HyperlinkedIdentityField(lookup_field='uuid', view_name='bottle-detail')
        uuid = UUIDField(read_only=True)
        creation_ts = DateTimeField(read_only=True)
        update_ts = DateTimeField(read_only=True)
        name = CharField(max_length=255)
        year = IntegerField(allow_null=True, required=False)
        alcohol = DecimalField(allow_null=True, decimal_places=1, max_digits=3, required=False)
        producer = HyperlinkedRelatedField(allow_null=True, lookup_field='uuid', queryset=Producer.objects.all(), required=False, view_name='producer-detail')
        vineyard_location = HyperlinkedRelatedField(allow_null=True, lookup_field='uuid', queryset=Location.objects.all(), required=False, view_name='location-detail')
    """
    class Meta:
        model = db_models.Bottle
        fields = '__all__'  # Or: exclude = ('year',)
        read_only_fields = ('uuid',)
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
