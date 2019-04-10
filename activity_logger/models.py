import uuid

from django.conf import settings
from django.contrib.gis.db import models
from django.utils.text import slugify
from django.utils.timezone import now


class Establishment(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    slug = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.updated_at = now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.slug

    class Meta:
        unique_together = ('slug', 'user')


class ActivityType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.updated_at = now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.slug

    class Meta:
        unique_together = ('slug', 'user')


class Activity(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    establishment = models.ForeignKey(Establishment, on_delete=models.PROTECT)
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.updated_at = now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.slug

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        permissions = (
            ('add', 'Add activities via API'),
            ('remove', 'Remove activities via API'),
        )
