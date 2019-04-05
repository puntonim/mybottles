from django.http import JsonResponse
from django.utils import timezone

from rest_framework import generics, mixins

from core import models as db_models

from . import serializers
from .domain_models import bottles_domain


def health(request):
    now = timezone.localtime(timezone.now())
    return JsonResponse({'date': now})


def unhealth(request):
    class UnhealthEndpointException(Exception):
        pass

    now = timezone.localtime(timezone.now())
    raise UnhealthEndpointException('/unhealth endpoint called on {}'.format(now))
    return 'It should have raised UnhealthTestException'


class BottleListView(generics.ListCreateAPIView):
    """
    GET
        $ curl 127.0.0.1:8000/api/bottles/
    POST
        $ curl 127.0.0.1:8000/api/bottles/ -d 'name=valp+classico&year=2019&producer=http://127.0.0.1:8000/api/producers/60321e2a-2d04-484f-8008-d874a590c4b6/'
        $ curl 127.0.0.1:8000/api/bottles/ -d '{"name":"valpo class", "year":2019}' -H 'Content-Type: application/json'
    """
    serializer_class = serializers.BottleSerializer
    queryset = db_models.Bottle.objects.order_by('-update_ts')


## Domain models version.
# class BottleListView(generics.ListAPIView):
#     """
#     $ curl "127.0.0.1:8000/api/bottles/"
#     """
#     serializer_class = serializers.BottleSerializer
#     domain_model_class = bottles_domain.BottlesListDomain
#
#     def get_queryset(self, *args, **kwargs):
#         self.domain_model = self.domain_model_class()
#         return self.domain_model.get_queryset()


class BottleDetailView(generics.RetrieveUpdateAPIView):
    """
    GET
        $ curl curl 127.0.0.1:8000/api/bottles/<uuid>/
    PATCH
        $ curl 127.0.0.1:8000/api/bottles/<uuid>/ -d '{"year":2019}' -X PATCH -H 'Content-Type: application/json'
    PUT
        $ curl 127.0.0.1:8000/api/bottles/<uuid>/ -d '{"name":"valpo class", "year":2019}' -X PUT -H 'Content-Type: application/json'
    """
    serializer_class = serializers.BottleSerializer
    queryset = db_models.Bottle.objects.all()
    lookup_field = 'uuid'


## Domain models version.
# class BottleDetailView(generics.RetrieveAPIView):
#     serializer_class = serializers.BottleSerializer
#     domain_model_class = bottles_domain.BottleDetailDomain
#
#     def get_object(self):
#         self.domain_model = self.domain_model_class()
#         return self.domain_model.get_object(self.kwargs['pk'])


class ProducerDetailView(generics.RetrieveUpdateAPIView):
    """
    GET
        $ curl 127.0.0.1:8000/api/producers/<uuid>/
    PATCH
        $ curl 127.0.0.1:8000/api/producers/<uuid>/ -d '{"winery_location":"newurl"}' -X PATCH -H 'Content-Type: application/json'
    PUT
        $ curl 127.0.0.1:8000/api/producers/<uuid>/ -d '{"name":"newname", "winery_location":"newurl"}' -X PUT -H 'Content-Type: application/json'
    """
    serializer_class = serializers.ProducerSerializer
    queryset = db_models.Producer.objects.all()
    lookup_field = 'uuid'


class LocationDetailView(generics.RetrieveUpdateAPIView):
    """
    GET
        $ curl 127.0.0.1:8000/api/locations/<uuid>/
    PATCH
        $ curl 127.0.0.1:8000/api/locations/<uuid>/ -d '{"name":"newname"}' -X PATCH -H 'Content-Type: application/json'
    PUT
        $ curl 127.0.0.1:8000/api/locations/<uuid>/ -d '{"name":"newname"}' -X PUT -H 'Content-Type: application/json'
    """
    serializer_class = serializers.LocationSerializer
    queryset = db_models.Location.objects.all()
    lookup_field = 'uuid'
