from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Create your views here.

from .models import Flight

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)

    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all()
    })


def book(request, flight_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login")
        return HttpResponseRedirect(reverse("users:login")+f"?next={request.path}")

    flight = get_object_or_404(Flight, pk=flight_id)
    #if request.user not in flight.passengers.all() and flight.is_seat_available():
    if request.user not in flight.passengers.all():
        flight.passengers.add(request.user)
    return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))
