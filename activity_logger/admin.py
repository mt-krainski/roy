from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Establishment, ActivityType, Activity


@admin.register(Establishment)
class EstablishmentAdmin(OSMGeoAdmin):
    list_display = ('name', 'location', 'updated_at')


@admin.register(ActivityType)
class ActivityTypeAdmin(ModelAdmin):
    list_display = ['name', 'updated_at']


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = [
        'uuid',
        'name',
        '_activity_type',
        '_establishment',
        'updated_at',
    ]

    def _activity_type(self, obj):
        return obj.activity_type.name

    def _establishment(self, obj):
        return obj.establishment.name

