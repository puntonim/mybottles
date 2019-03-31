from django.contrib import admin

from . import models


BOTTLEADMIN_READONLY_FIELDS = ('creation_ts', 'update_ts')


class BottleAdmin(admin.ModelAdmin):
    readonly_fields = BOTTLEADMIN_READONLY_FIELDS
    fields = [field.name for field in models.Bottle._meta.fields if field.name not in ('id', ) + BOTTLEADMIN_READONLY_FIELDS]


admin.site.register(models.Bottle, BottleAdmin)
admin.site.register(models.Producer)
admin.site.register(models.Location)
admin.site.register(models.Store)
admin.site.register(models.Purchase)
admin.site.register(models.Photo)
