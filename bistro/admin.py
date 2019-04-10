from django.contrib import admin

# Register your models here.
from .models import BistroPlace, BistroType, Visit, ConsumableType

admin.site.register(BistroPlace)
admin.site.register(BistroType)
admin.site.register(Visit)
admin.site.register(ConsumableType)