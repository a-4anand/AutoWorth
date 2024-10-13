

from django import forms
from .models import VehicleListing

class VehicleListingForm(forms.ModelForm):
    class Meta:
        model = VehicleListing
        fields = ['make', 'model', 'year', 'fuel_type','car_rating','body_type', 'total_owners','registered_city','varient','registered_state','warranty_avail','fitness_certificate','transmission', 'kms_run', 'price', 'description', 'image']
