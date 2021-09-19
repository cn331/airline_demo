from django.test import TestCase

# Create your tests here.

from .models import Airport, Flight
from django.contrib.auth.models import User

class FlightTestCase(TestCase):

    def setUp(self):

        # create airports
        airport1 = Airport.objects.create(code="AAA", city="City A")
        airport2 = Airport.objects.create(code="BBB", city="City B")

        Flight.objects.create(origin=airport1, destination=airport2, duration=400)

    def test_seat_available(self):
        """ is_seat_available should be True """

        flight = Flight.objects.first()

        self.assertTrue(flight.is_seat_available())

    def test_seat_not_available(self):
        """ is_seat_available should be False"""

        user1 = User.objects.create(username="user1", password="1234", email="user1@example.com")
        user2 = User.objects.create(username="user2", password="1234", email="user2@example.com")

        flight = Flight.objects.first()
        flight.passengers.add(user1)
        flight.passengers.add(user2)

        self.assertFalse(flight.is_seat_available())