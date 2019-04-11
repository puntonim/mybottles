from haystack import indexes

from .models import Bottle


class BottleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # These extra fields are for filtering (eg. filtering by date).
    vineyard_location = indexes.CharField(model_attr='vineyard_location__name')
    update_ts = indexes.DateTimeField(model_attr='update_ts')

    def get_model(self):
        return Bottle

    # def index_queryset(self, using=None):
    #     """Used when the entire index for model is updated."""
    #     return self.get_model().objects.filter(update_ts__lte=datetime.datetime.now())
