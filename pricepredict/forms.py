
from .models import BikeListing
from django import forms
from .models import VehicleListing

class VehicleListingForm(forms.ModelForm):
    class Meta:
        model = VehicleListing
        fields = ['phone_no','make', 'model', 'year', 'fuel_type','car_rating','body_type', 'total_owners','registered_city','varient','registered_state','warranty_avail','fitness_certificate','transmission', 'kms_run', 'price', 'description', 'image']


# added for bike price prediction by anand dubey @ 9nov 2024

class BikePriceForm(forms.Form):
    bike_name = forms.CharField(label='Bike Name')
    city = forms.CharField(label='City')
    kms_driven = forms.IntegerField(label='Kilometers Driven')
    owner = forms.CharField(label='Owner Type [First Owner/Second Owner .etc]')
    age = forms.IntegerField(label='Age of Bike')
    power = forms.IntegerField(label='Power (cc)')
    brand = forms.CharField(label='Brand')


class BikeListingForm(forms.ModelForm):
    class Meta:
        model = BikeListing
        fields = ['phone_no', 'company', 'engine_capacity','model', 'year', 'bike_rating', 'total_owners', 'registered_city', 'registered_state', 'warranty_avail', 'fitness_certificate', 'kms_run', 'price', 'description', 'image']