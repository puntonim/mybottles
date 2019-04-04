import uuid

from django.db import models


class Bottle(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    creation_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    producer = models.ForeignKey('Producer', on_delete=models.SET_NULL, blank=True, null=True)
    vineyard_location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    alcohol = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        pretty = '{}|{}'.format(self.id, self.name)
        if self.producer and self.producer.name:
            pretty += '|' + self.producer.name
        if self.year:
            pretty += '|' + str(self.year)
        return pretty


class Producer(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    winery_location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = (('name', 'winery_location'),)

    def __str__(self):
        pretty = '{}|{}'.format(self.id, self.name)
        if self.winery_location:
            pretty += '|' + str(self.winery_location.name)
        return pretty


class Location(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    # Examples: Alba, Valpolicella, Jesi.
    name = models.CharField(max_length=255, unique=True)

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
    date = models.DateTimeField(blank=True, null=True)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)

    def __str__(self):
        return '{}|bottle={}'.format(self.id, self.bottle)


class Photo(models.Model):
    bottle = models.ForeignKey('Bottle', on_delete=models.CASCADE)
    file = models.FileField(upload_to='photos/')

    def __str__(self):
        return '{}|bottle={}'.format(self.id, self.bottle)
