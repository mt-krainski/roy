from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Establishment


@admin.register(Establishment)
class EstablishmentAdmin(OSMGeoAdmin):
    list_display = ('name', 'location', 'updated_at')
