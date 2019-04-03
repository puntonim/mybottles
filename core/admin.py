from django.contrib import admin

from . import models


READONLY_FIELDS = ('creation_ts', 'update_ts', 'uuid')


def ReadOnlyFieldsAdminBase(model):
    class _ReadOnlyFieldsAdminBase(admin.ModelAdmin):
        readonly_fields = [field.name for field in model._meta.fields if field.name in READONLY_FIELDS]
        fields = [field.name for field in model._meta.fields if field.name not in ('id',)]
    return _ReadOnlyFieldsAdminBase


admin.site.register(models.Bottle, ReadOnlyFieldsAdminBase(models.Bottle))
admin.site.register(models.Producer, ReadOnlyFieldsAdminBase(models.Producer))
admin.site.register(models.Location, ReadOnlyFieldsAdminBase(models.Location))
admin.site.register(models.Store, ReadOnlyFieldsAdminBase(models.Store))
admin.site.register(models.Purchase, ReadOnlyFieldsAdminBase(models.Purchase))
admin.site.register(models.Photo)
