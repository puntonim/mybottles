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

        ## Simplest query.
        # sqs = SearchQuerySet().auto_query(q)

        # `.filter` is used to allow the auto_query functionality and also allow start search with star, negation
        # and sentence, like: DOC* -DOCG -"Barolo DOCG Langhe"
        # `.models` is used to limit the search on a specific model (Bottle, Location, ...).
        # sqs = SearchQuerySet().models(queryset.model).filter(content=Raw(str(AutoQuery(q))))
        sqs = SearchQuerySet().models(queryset.model).filter_or(content=AutoQuery(q))
        return queryset.filter(id__in=[res.pk for res in sqs])
