from rest_framework import serializers

from core.models import Bottle

# TODO consider serpy to speed up the serialization:
# https://github.com/clarkduvall/serpy


class BottleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bottle
        fields = '__all__'
