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
    """
    >>> BottleSerializerDetailed():
        url = HyperlinkedIdentityField(lookup_field='uuid', view_name='bottle-detail')
        uuid = UUIDField(read_only=True)
        update_ts = DateTimeField(read_only=True)
        name = CharField(max_length=255)
        producer = HyperlinkedRelatedField(allow_null=True, lookup_field='uuid', queryset=Producer.objects.all(), required=False, view_name='producer-detail')
        vineyard_location = HyperlinkedRelatedField(allow_null=True, lookup_field='uuid', queryset=Location.objects.all(), required=False, view_name='location-detail')
        year = IntegerField(allow_null=True, required=False)
        alcohol = DecimalField(allow_null=True, decimal_places=1, max_digits=3, required=False)
        producer_details = ProducerSerializerDetailed(read_only=True, source='producer'):
            url = HyperlinkedIdentityField(lookup_field='uuid', view_name='producer-detail')
            uuid = UUIDField(read_only=True)
            name = CharField(max_length=255)
            winery_location = HyperlinkedRelatedField(allow_null=True, lookup_field='uuid', queryset=Location.objects.all(), required=False, view_name='location-detail')
            winery_location_details = LocationSerializer(read_only=True, source='winery_location'):
                url = HyperlinkedIdentityField(lookup_field='uuid', view_name='location-detail')
                uuid = UUIDField(read_only=True)
                name = CharField(max_length=255, validators=[<UniqueValidator(queryset=Location.objects.all())>])
        vineyard_location_details = LocationSerializer(read_only=True, source='vineyard_location'):
            url = HyperlinkedIdentityField(lookup_field='uuid', view_name='location-detail')
            uuid = UUIDField(read_only=True)
            name = CharField(max_length=255, validators=[<UniqueValidator(queryset=Location.objects.all())>])
        photos = SerializerMethodField(read_only=True)
    """  # noqa E501
    producer_details = ProducerSerializerDetailed(read_only=True, source='producer')
    vineyard_location_details = LocationSerializer(read_only=True, source='vineyard_location')
    photos = serializers.SerializerMethodField(read_only=True)

    class Meta(BottleSerializer.Meta):
        fields = BottleSerializer.Meta.fields + ('producer_details', 'vineyard_location_details', 'photos')

    def get_photos(self, obj):
        return [photo.file.url for photo in obj.photo_set.all()]


class PhotoSerializer(serializers.ModelSerializer):
    bottle = serializers.HyperlinkedRelatedField(
        lookup_field='uuid', queryset=db_models.Bottle.objects.all(), view_name='bottle-detail')

    class Meta:
        model = db_models.Photo
        exclude = ('id', )
