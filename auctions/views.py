from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from auctions.models import Listing, Bid, Comment, Category


def index(request):
    return render(request, "auctions/index.html")


def createListings(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {
            "message": "You should login first."
        })
    if request.method == "POST":
        l_title = request.POST["title"]
        l_description = request.POST["description"]
        l_bid = request.POST["bid"]
        l_img_url = request.POST["url"]
        l_category = request.POST["category"]
        l_publisher = request.user.username

        listing = Listing(title=l_title, description=l_description,
                          image_url=l_img_url, publisher=l_publisher)
        listing.save()

        bid = Bid(bid=l_bid, listing_id=listing.pk)
        bid.sava()

        categroy = Category(category=l_category, listing_id=listing.pk)
        categroy.save()

        return HttpResponseRedirect(reverse("listing", listing.pk))
    return render(request, "auctions/createListings.html")


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", lis ting)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
