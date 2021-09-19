from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Max

from .models import Airport, Flight
from django.contrib.auth.models import User

class FlightViewTestCase(TestCase):

    def setUp(self):

        # create airports
        airport1 = Airport.objects.create(code="AAA", city="City A")
        airport2 = Airport.objects.create(code="BBB", city="City B")

        flight = Flight.objects.create(origin=airport1, destination=airport2, duration=400)
        user = User.objects.create(username="user1", password="1234", email="user1@example.com")
        flight.passengers.add(user)

    def test_index_view_status_code(self):
        """ index view's status code is ok """

        c = Client()
        response = c.get(reverse('flights:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        """ context is correctly set """

        c = Client()
        response = c.get(reverse('flights:index'))
        self.assertEqual(response.context['flights'].count(), Flight.objects.count())

    def test_valid_flight_page(self):
        """ valid flight page should return status code 200 """

        c = Client()
        f = Flight.objects.first()
        response = c.get(reverse('flights:flight', args=(f.id,)))
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        """ invalid flight page should return status code 404 """

        max_id = Flight.objects.all().aggregate(Max("id"))['id__max']

        c = Client()
        response = c.get(reverse('flights:flight', args=(max_id+1,)))
        self.assertEqual(response.status_code, 404)

    def test_guest_user_cannot_book_flight(self):
        """ guest cannot book a flight """
        user = User.objects.create(username="user2", password="1234", email="user2@example.com")
        f = Flight.objects.first()

        c = Client()
        response = c.get(reverse('flights:book', args=(f.id,)))
        self.assertEqual(f.passengers.count(), 1)

    def test_authenticated_user_can_book_flight(self):
        """ authenticated user can book a flight """
        user = User.objects.create(username="user2", password="1234", email="user2@example.com")
        f = Flight.objects.first()

        c = Client()
        c.force_login(user)
        response = c.get(reverse('flights:book', args=(f.id,)))
        self.assertEqual(f.passengers.count(), 2)


    def test_cannot_book_nonavailable_seat_flight(self):
        """ cannot book full capacity flight"""
        self.test_authenticated_user_can_book_flight()

        user = User.objects.create(username="user3", password="1234", email="user3@example.com")
        f = Flight.objects.first()

        c = Client()
        c.force_login(user)
        response = c.get(reverse('flights:book', args=(f.id,)))
        self.assertEqual(f.passengers.count(), 2)