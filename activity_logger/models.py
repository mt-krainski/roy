from django.contrib.gis.db import models
from django.utils.text import slugify
from django.utils.timezone import now


class Establishment(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    slug = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug= slugify(self.name)
        self.updated_at = now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.slug


class ActivityType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.updated_at = now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.slug


class Activity(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    establishment = models.ForeignKey(Establishment, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.updated_at = now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.slug
