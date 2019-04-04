from django.contrib import admin

from . import models


DEFAULT_READONLY_FIELDS = ('creation_ts', 'update_ts', 'uuid')
DEFAULT_SEARCH_FIELDS = ('uuid', 'name')


def ReadOnlyFieldsAdminBase(model):
    class _ReadOnlyFieldsAdminBase(admin.ModelAdmin):
        readonly_fields = [field.name for field in model._meta.fields if field.name in DEFAULT_READONLY_FIELDS]
        fields = [field.name for field in model._meta.fields if field.name not in ('id',)]
        search_fields = [field.name for field in model._meta.fields if field.name in DEFAULT_SEARCH_FIELDS]
    return _ReadOnlyFieldsAdminBase


class BottleAdmin(ReadOnlyFieldsAdminBase(models.Bottle)):
    list_display = ('update_ts', 'name', 'producer_name', 'year')
    ordering = ('-update_ts', )
    autocomplete_fields = ('producer', 'vineyard_location')

    def producer_name(self, obj):
        return obj.producer.name if obj.producer else None


class ProducerAdmin(ReadOnlyFieldsAdminBase(models.Producer)):
    list_display = ('name', 'winery_location_name')
    autocomplete_fields = ('winery_location',)

    def winery_location_name(self, obj):
        return obj.winery_location.name if obj.winery_location else None


admin.site.register(models.Bottle, BottleAdmin)
admin.site.register(models.Producer, ProducerAdmin)
admin.site.register(models.Location, ReadOnlyFieldsAdminBase(models.Location))
admin.site.register(models.Store, ReadOnlyFieldsAdminBase(models.Store))
admin.site.register(models.Purchase, ReadOnlyFieldsAdminBase(models.Purchase))
admin.site.register(models.Photo)
