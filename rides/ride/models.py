
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('rider', 'Rider'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='rider')

    def __str__(self):
        return self.username


# Create your models here.
class Ride(models.Model):
    STATUS_CHOICES = (
        ('en-route', 'En-route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
    )
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    id_driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_rides')
    id_rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rider_rides')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"Ride {self.id_ride}: {self.status}"


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, related_name="ride_events", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RideEvent {self.id_ride_event} for Ride {self.id_ride.id_ride}"