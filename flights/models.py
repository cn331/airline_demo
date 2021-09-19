from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()
    passengers = models.ManyToManyField(User, blank=True, related_name="flights")
    capacity = models.PositiveIntegerField(default=2)

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

    def is_seat_available(self):
        return self.passengers.count() < self.capacity

