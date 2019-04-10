import uuid

from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as gis_models


class Type(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)


class ConsumableType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)


class Place(gis_models.Model):
    name = gis_models.CharField(max_length=100)
    slug = gis_models.CharField(max_length=100, blank=True)
    location = gis_models.PointField()
    user = gis_models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=gis_models.CASCADE)
    type = gis_models.ForeignKey(
        Type, on_delete=gis_models.PROTECT)
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )


class Visit(models.Model):
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=(
            (1, '⭐'),
            (2, '⭐⭐'),
            (3, '⭐⭐⭐'),
            (4, '⭐⭐⭐⭐'),
            (5, '⭐⭐⭐⭐⭐'),
        )
    )
    consumable = models.ForeignKey(ConsumableType, on_delete=models.PROTECT)
    price = models.FloatField()
