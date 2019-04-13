from haystack import indexes
from haystack.signals import RealtimeSignalProcessor

from . import models


class BottleIndex(indexes.SearchIndex, indexes.Indexable):
    ## Template version, see: http://docs.haystacksearch.org/en/master/tutorial.html#creating-searchindexes
    ## Using template in: core/templates/search/indexes/core/bottle_text.txt
    # text = indexes.CharField(document=True, use_template=True)
    # Method version.
    text = indexes.CharField(document=True)

    # Extra fields used for search filtering (eg. filtering by date).
    # See: http://docs.haystacksearch.org/en/master/best_practices.html#additional-fields-for-filtering
    # It can also be used as timestamp in Kibana.
    update_ts = indexes.DateTimeField(model_attr='update_ts')
    # year = indexes.IntegerField(model_attr='year')
    # vineyard_location = indexes.CharField(model_attr='vineyard_location__name')

    ## Extra fields stored in ES, but not indexed. Useful for avoiding hitting the db.
    ## See: http://docs.haystacksearch.org/en/master/best_practices.html#avoid-hitting-the-database
    ## And: http://docs.haystacksearch.org/en/master/searchindex_api.html#stored-indexed-fields
    # year = indexes.IntegerField(model_attr='year', indexed=False, null=True)
    ## Unfortunately there is no object type that would let JSON to be stored.
    # photos = indexes.MultiValueField(indexed=False)
    # def prepare_photos(self, obj):
    #     return [photo.file.url for photo in obj.photo_set.all()]

    def get_model(self):
        return models.Bottle

    # def index_queryset(self, using=None):
    #     """Used when the entire index for model is updated. You can use it to avoid indexing
    #     data that is in the db but not public yet (because it has a publication date in the future)."""
    #     return self.get_model().objects.filter(update_ts__lte=datetime.datetime.now())

    def prepare_text(self, obj):
        data = [obj.name]
        if obj.producer:
            data.append(obj.producer.name)
            if obj.producer.winery_location:
                data.append(obj.producer.winery_location.name)
        if obj.vineyard_location:
            data.append(obj.vineyard_location.name)
        for purchase in obj.purchase_set.all():
            if purchase.notes:
                data.append(purchase.notes)
        return '\n'.join(data)


class LocationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='name')

    def get_model(self):
        return models.Location


class RealTimeIndexerSignalProcessor(RealtimeSignalProcessor):
    """
    The stock RealtimeSignalProcessor works well only if the models itself is saved/deleted.
    BottleIndex includes a related field (Purchase.notes) and so we need to reindex BottleIndex
    also when the related Purchase is saved/deleted.
    """
    def handle_save(self, sender, instance, **kwargs):
        using_backends = self.connection_router.for_write(instance=instance)
        for using in using_backends:
            if sender == models.Purchase:
                BottleIndex().update_object(instance.bottle, using=using)
        return super().handle_save(sender, instance, **kwargs)

    def handle_delete(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        delete should be sent to & delete the object on those backends.
        """
        using_backends = self.connection_router.for_write(instance=instance)
        for using in using_backends:
            if sender == models.Purchase:
                # No need to remove the bottle, but update it.
                # BottleIndex().remove_object(instance.bottle, using=using)
                BottleIndex().update_object(instance.bottle, using=using)
        return super().handle_delete(sender, instance, **kwargs)
