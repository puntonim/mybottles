from django.db import models


class Bottle(models.Model):
    creation_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    producer = models.ForeignKey('Producer', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    alcohol = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return '{}|{}'.format(self.id, self.name)


class Producer(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '{}|{}'.format(self.id, self.name)


class Location(models.Model):
    # Examples: Alba, Valpolicella, Jesi.
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}|{}'.format(self.id, self.name)


class Store(models.Model):
    # Examples: IPER Brembate, Carrefour Zingonia.
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}|{}'.format(self.id, self.name)


class Purchase(models.Model):
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
