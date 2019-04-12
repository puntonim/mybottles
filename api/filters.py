from haystack.inputs import AutoQuery, Raw
from haystack.query import SearchQuerySet
from rest_framework import filters


class SearchFilterBackend(filters.BaseFilterBackend):
    """
    Search against Elasticsearch with django-haystack.
    """
    def filter_queryset(self, request, queryset, view):
        q = request.query_params.get('q')
        if not q:
            return queryset
        # sqs = SearchQuerySet().auto_query(q)
        # Use the auto_query functionality and also allow start search like: DOC* -DOCG -"Barolo DOCG Langhe"
        sqs = SearchQuerySet().filter(content=Raw(str(AutoQuery(q))))
        return queryset.filter(id__in=[res.pk for res in sqs])
