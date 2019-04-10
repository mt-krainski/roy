from django.contrib.gis import forms

from bistro.models import BistroType


class PlaceForm(forms.Form):
    place_name = forms.CharField(
        label='Place Name',
        max_length=100
    )
    type = forms.ModelChoiceField(
        label='Place Type',
        queryset=BistroType.objects.all()
    )