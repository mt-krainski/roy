from django.contrib.gis import forms

from .models import BistroType
from .widgets import BootstrapMapWidget


class PlaceForm(forms.Form):
    place_name = forms.CharField(
        label='Place Name',
        max_length=100
    )
    type = forms.ModelChoiceField(
        label='Place Type',
        queryset=BistroType.objects.all()
    )
    location = forms.PointField(
        widget=BootstrapMapWidget(),
        required=False
    )
