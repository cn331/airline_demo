from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    else:
        return render(request, "users/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET["next"])
        else:
            messages.warning(request, "Invalid credential.")
            return render(request, "users/login.html", {
                "messages": messages.get_messages(request)
            })

    if "next" in request.GET:
        next = request.GET["next"]
    else:
        next = reverse("users:index")

    return render(request, "users/login.html", {
        "next": next
    })

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")
    return render(request, "users/login.html", {
        "messages": messages.get_messages(request)
    })