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


class BottleListView(generics.ListAPIView):
    """
    $ curl 127.0.0.1:8000/api/bottles/
    """
    serializer_class = serializers.BottleSerializer
    queryset = db_models.Bottle.objects.all()


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


class BottleDetailView(generics.RetrieveAPIView):
    """
    $ curl curl 127.0.0.1:8000/api/bottles/1/
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


class ProducerDetailView(generics.RetrieveAPIView):
    """
    $ curl 127.0.0.1:8000/api/producers/1/
    """
    serializer_class = serializers.ProducerSerializer
    queryset = db_models.Producer.objects.all()
    lookup_field = 'uuid'


class LocationDetailView(generics.RetrieveAPIView):
    """
    $ curl 127.0.0.1:8000/api/locations/1/
    """
    serializer_class = serializers.LocationSerializer
    queryset = db_models.Location.objects.all()
    lookup_field = 'uuid'
