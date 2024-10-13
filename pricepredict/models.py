from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FuelType(models.TextChoices):
    PETROL = 'petrol', 'Petrol'
    DIESEL = 'diesel', 'Diesel'
    ELECTRIC = 'electric', 'Electric'
    HYBRID = 'hybrid', 'Hybrid'

class TransmissionType(models.TextChoices):
    MANUAL = 'manual', 'Manual'
    AUTOMATIC = 'automatic', 'Automatic'

class BodyType(models.TextChoices):
    SEDAN = 'sedan', 'Sedan'
    SUV = 'suv', 'SUV'
    HATCHBACK = 'hatchback', 'Hatchback'
    COUPE = 'coupe', 'Coupe'




class VehicleListing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(
        max_length=10,
        choices=FuelType.choices,
        default=FuelType.PETROL
    )
    transmission = models.CharField(
        max_length=10,
        choices=TransmissionType.choices,
        default=TransmissionType.MANUAL
    )
    kms_run = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    body_type = models.CharField(
        max_length=10,
        choices=BodyType.choices,
        default=BodyType.SEDAN
    )

    class CarRating(models.TextChoices):
        GREAT = 'great', 'Great'
        GOOD = 'good', 'Good'
        FAIR = 'fair', 'Fair'
        OVERPRICED = 'overpriced', 'Overpriced'

    total_owners = models.IntegerField()
    registered_city = models.CharField(max_length=100)
    registered_state = models.CharField(max_length=100)
    warranty_avail = models.BooleanField(default=False)
    fitness_certificate = models.BooleanField(default=False)
    varient=models.CharField(max_length=100)
    car_rating = models.CharField(
        max_length=15,
        choices=CarRating.choices,
        default=CarRating.GOOD,
    )



    def __str__(self):
        return f"{self.make} {self.model} - {self.year}"

class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_listing = models.ForeignKey('VehicleListing', related_name='interests', on_delete=models.CASCADE)
    message = models.TextField()
    interest_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interest by {self.user.username} in {self.car_listing.make} {self.car_listing.model}"
