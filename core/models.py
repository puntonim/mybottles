import uuid

from django.core.exceptions import ValidationError
from django.db import models

from api import validators


class Bottle(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    creation_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    producer = models.ForeignKey('Producer', on_delete=models.SET_NULL, blank=True, null=True)
    vineyard_location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    alcohol = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('bottle-detail', kwargs=dict(uuid=self.uuid))

    def __str__(self):
        pretty = '{}|{}'.format(self.id, self.name)
        if self.producer and self.producer.name:
            pretty += '|' + self.producer.name
        if self.year:
            pretty += '|' + str(self.year)
        return pretty


class Producer(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    winery_location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('producer-detail', kwargs=dict(uuid=self.uuid))

    def __str__(self):
        pretty = '{}|{}'.format(self.id, self.name)
        if self.winery_location:
            pretty += '|' + str(self.winery_location.name)
        return pretty


class Location(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    # Examples: Alba, Valpolicella, Jesi.
    name = models.CharField(max_length=255, unique=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('location-detail', kwargs=dict(uuid=self.uuid))

    def __str__(self):
        return '{}|{}'.format(self.id, self.name)


class Store(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    # Examples: IPER Brembate, Carrefour Zingonia.
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '{}|{}'.format(self.id, self.name)


class Purchase(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    bottle = models.ForeignKey('Bottle', on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    price_paid = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    price_original = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, blank=True, null=True)
    is_gift = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '{}|bottle={}'.format(self.id, self.bottle)

    def clean(self, *args, **kwargs):
        """
        Validation for Model forms and Django Admin forms. This method is automatically called in any Model form.
        Note: this is not called by `obj.save()` by default. But this behavior has been intentionally added by
        overriding `save()`.
        """
        # Use the same validator as the DJRF API serializer does.
        data = {}
        for key in [field.name for field in self._meta.fields]:
            data[key] = getattr(self, key)
        validators.validate_purchase(data, ValidationError)
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Add the validation step by calling `self.clean()` (the same validation step that a Model form (like Django
        # Admin ones do).
        self.clean()
        return super().save(*args, **kwargs)


class Photo(models.Model):
    bottle = models.ForeignKey('Bottle', on_delete=models.CASCADE)
    file = models.FileField(upload_to='photos/')

    def __str__(self):
        return '{}|bottle={}'.format(self.id, self.bottle)
