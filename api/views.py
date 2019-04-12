from urllib.parse import parse_qs

from django.http import JsonResponse
from django.utils import timezone
from haystack.query import SearchQuerySet
from rest_framework import generics

from core import models as db_models

from . import filters, serializers


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
    """  # noqa E501
    serializer_class = serializers.BottleSerializer
    queryset = db_models.Bottle.objects.order_by('-update_ts')
    filter_backends = (filters.SearchFilterBackend,)


class BottleDetailView(generics.RetrieveUpdateAPIView):
    """
    GET
        $ curl curl 127.0.0.1:8000/api/bottles/<uuid>/
    PATCH
        $ curl 127.0.0.1:8000/api/bottles/<uuid>/ -d '{"year":2019}' -X PATCH -H 'Content-Type: application/json'
    PUT
        $ curl 127.0.0.1:8000/api/bottles/<uuid>/ -d '{"name":"valpo class", "year":2019}' -X PUT -H 'Content-Type: application/json'
    """  # noqa E501
    serializer_class = serializers.BottleSerializerDetailed
    queryset = db_models.Bottle.objects.all()
    lookup_field = 'uuid'


class ProducerListView(generics.ListCreateAPIView):
    """
    GET
        $ curl 127.0.0.1:8000/api/producers/
    POST
        $ curl 127.0.0.1:8000/api/producers/ -d '{"name":"bolla"}' -H 'Content-Type: application/json'
    """  # noqa E501
    serializer_class = serializers.ProducerSerializer
    queryset = db_models.Producer.objects.order_by('-id')


class ProducerDetailView(generics.RetrieveUpdateAPIView):
    """
    GET
        $ curl 127.0.0.1:8000/api/producers/<uuid>/
    PATCH
        $ curl 127.0.0.1:8000/api/producers/<uuid>/ -d '{"winery_location":"newurl"}' -X PATCH -H 'Content-Type: application/json'
    PUT
        $ curl 127.0.0.1:8000/api/producers/<uuid>/ -d '{"name":"newname", "winery_location":"newurl"}' -X PUT -H 'Content-Type: application/json'
    """  # noqa E501
    serializer_class = serializers.ProducerSerializerDetailed
    queryset = db_models.Producer.objects.all()
    lookup_field = 'uuid'


class LocationListView(generics.ListCreateAPIView):
    """
    GET
        $ curl 127.0.0.1:8000/api/locations/
    POST
        $ curl 127.0.0.1:8000/api/locations/ -d '{"name":"alba"}' -H 'Content-Type: application/json'
    """
    serializer_class = serializers.LocationSerializer
    queryset = db_models.Location.objects.order_by('-id')


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


class PhotoListView(generics.CreateAPIView):
    """
    POST
        $ curl 127.0.0.1:8000/api/photos/ -F "bottle=http://127.0.0.1:8000/api/bottles/9ec758ae-f380-428c-b380-109476b13b6d/" -F "file=@/tmp/img.jpg"
    """  # noqa E501
    serializer_class = serializers.PhotoSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # The response is an empty 201.
        response.data = None
        return response


class StoreListView(generics.ListCreateAPIView):
    """
    GET
        $ curl 127.0.0.1:8000/api/stores/
    POST
        $ curl 127.0.0.1:8000/api/stores/ -d '{"name":"iper brembate"}' -H 'Content-Type: application/json'
    """  # noqa E501
    serializer_class = serializers.StoreSerializer
    queryset = db_models.Store.objects.order_by('-id')


class StoreDetailView(generics.RetrieveUpdateAPIView):
    """
    GET
        $ curl curl 127.0.0.1:8000/api/stores/<uuid>/
    PATCH
        $ curl 127.0.0.1:8000/api/stores/<uuid>/ -d '{"name":"iper brembate"}' -X PATCH -H 'Content-Type: application/json'
    PUT
        $ curl 127.0.0.1:8000/api/stores/<uuid>/ -d '{"name":"iper brembate"}' -X PUT -H 'Content-Type: application/json'
    """  # noqa E501
    serializer_class = serializers.StoreSerializer
    queryset = db_models.Store.objects.all()
    lookup_field = 'uuid'


class PurchaseListView(generics.CreateAPIView):
    """
    POST
        $ curl 127.0.0.1:8000/api/purchases/ -d '"{bottle":"http://127.0.0.1:8000/api/bottles/9ec758ae-f380-428c-b380-109476b13b6d/", "store":"http://127.0.0.1:8000/api/stores/0tr658ae-f380-428c-b380-109476b13j2f/"}' -H 'Content-Type: application/json'
    """  # noqa E501
    serializer_class = serializers.PurchaseSerializer


class PurchaseDetailView(generics.RetrieveUpdateAPIView):
    """
    GET
        $ curl curl 127.0.0.1:8000/api/purchases/<uuid>/
    PATCH
        $ curl 127.0.0.1:8000/api/purchases/<uuid>/ -d '{"quantity":2}' -X PATCH -H 'Content-Type: application/json'
    PUT
        $ curl 127.0.0.1:8000/api/purchases/<uuid>/ -d '{"quantity":2, "bottle":"http://127.0.0.1:8000/api/bottles/9ec758ae-f380-428c-b380-109476b13b6d/", "store":"http://127.0.0.1:8000/api/stores/0tr658ae-f380-428c-b380-109476b13j2f/"}' -X PUT -H 'Content-Type: application/json'
    """  # noqa E501
    serializer_class = serializers.PurchaseSerializerDetailed
    queryset = db_models.Purchase.objects.all()
    lookup_field = 'uuid'


def search_test(request):
    # TODO keep it?
    q = ' '.join(parse_qs(request.META['QUERY_STRING']).get('q'))
    sqs = SearchQuerySet().auto_query(q)
    return JsonResponse({'results': [str(res.object.__dict__) for res in sqs]})
