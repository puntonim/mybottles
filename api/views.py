from django.http import JsonResponse
from django.utils import timezone

from rest_framework import generics

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


class BottlesListView(generics.ListAPIView):
    """
    $ curl "127.0.0.1:8000/api/bottles/"
    """
    serializer_class = serializers.BottleSerializer
    domain_model_class = bottles_domain.BottlesListDomain

    def get_queryset(self, *args, **kwargs):
        self.domain_model = self.domain_model_class()
        return self.domain_model.get_queryset()
