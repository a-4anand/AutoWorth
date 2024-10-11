

from django import forms
from .models import VehicleListing

class VehicleListingForm(forms.ModelForm):
    class Meta:
        model = VehicleListing
        fields = ['make', 'model', 'year', 'fuel_type', 'transmission', 'kms_run', 'price', 'description', 'image']
