import uuid

from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils.text import slugify


class BistroType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ConsumableType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class BistroPlace(gis_models.Model):
    name = gis_models.CharField(max_length=100)
    slug = gis_models.CharField(max_length=100, blank=True)
    location = gis_models.PointField(blank=True, null=True)
    user = gis_models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=gis_models.CASCADE)
    type = gis_models.ForeignKey(
        BistroType, on_delete=gis_models.PROTECT)
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Visit(models.Model):
    place = models.ForeignKey(BistroPlace, on_delete=models.PROTECT)
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
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
