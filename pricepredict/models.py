from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class VehicleListing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    kms_run = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} - {self.year}"

class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_listing = models.ForeignKey('VehicleListing', related_name='interests', on_delete=models.CASCADE)
    message = models.TextField()
    interest_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interest by {self.user.username} in {self.car_listing.make} {self.car_listing.model}"
