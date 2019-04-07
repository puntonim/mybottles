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


class PhotoInline(admin.TabularInline):
    model = models.Photo
    show_change_link = True
    has_add_permission = lambda self, request, obj: False  # noqa E731
    has_change_permission = lambda self, request, obj: False  # noqa E731
    has_delete_permission = lambda self, request, obj: False  # noqa E731


class PurchaseInline(admin.TabularInline):
    model = models.Purchase
    show_change_link = True
    has_add_permission = lambda self, request, obj: False  # noqa E731
    has_change_permission = lambda self, request, obj: False  # noqa E731
    has_delete_permission = lambda self, request, obj: False  # noqa E731


class BottleAdmin(ReadOnlyFieldsAdminBase(models.Bottle)):
    list_display = ('update_ts', 'name', 'producer_name', 'year')
    ordering = ('-update_ts', )
    autocomplete_fields = ('producer', 'vineyard_location')
    inlines = (PhotoInline, PurchaseInline)

    def producer_name(self, obj):
        return obj.producer.name if obj.producer else None


class ProducerAdmin(ReadOnlyFieldsAdminBase(models.Producer)):
    list_display = ('name', 'winery_location_name')
    autocomplete_fields = ('winery_location',)

    def winery_location_name(self, obj):
        return obj.winery_location.name if obj.winery_location else None


class PurchaseAdmin(ReadOnlyFieldsAdminBase(models.Purchase)):
    list_display = ('date', 'bottle', 'store', 'quantity', 'price_paid')
    autocomplete_fields = ('bottle', 'store')


class StoreAdmin(ReadOnlyFieldsAdminBase(models.Store)):
    list_display = ('name',)


class LocationAdmin(ReadOnlyFieldsAdminBase(models.Location)):
    list_display = ('name',)


class PhotoAdmin(ReadOnlyFieldsAdminBase(models.Photo)):
    list_display = ('file',)


admin.site.register(models.Bottle, BottleAdmin)
admin.site.register(models.Producer, ProducerAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Store, StoreAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.Photo, PhotoAdmin)
