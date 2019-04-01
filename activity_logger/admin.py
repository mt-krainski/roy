from datetime import timedelta

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Establishment, ActivityType, Activity


@admin.register(Establishment)
class EstablishmentAdmin(OSMGeoAdmin):
    list_display = ('name', 'location', 'updated_at', '_user')
    fields = ('name', 'location', 'user')

    def _user(self, obj):
        return obj.user.username if obj.user else '--'


@admin.register(ActivityType)
class ActivityTypeAdmin(ModelAdmin):
    list_display = ('name', 'updated_at')


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = (
        '_uuid_short',
        '_user',
        'name',
        '_activity_type',
        '_establishment',
        'updated_at',
        'start_time',
        'end_time',
        '_duration'
    )

    list_filter = (
        'activity_type',
        'user'
    )

    def _uuid_short(self, obj):
        return str(obj.uuid).split('-')[0]
    _uuid_short.short_description = 'UUID'

    def _user(self, obj):
        return obj.user.username if obj.user else '--'

    def _activity_type(self, obj):
        return obj.activity_type.name

    def _establishment(self, obj):
        return obj.establishment.name

    def _duration(self, obj):
        if obj.start_time is not None and obj.end_time is not None:
            duration = obj.end_time - obj.start_time
            return duration - timedelta(microseconds=duration.microseconds)

        return '--'
