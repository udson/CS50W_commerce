from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import ListingForm
from .models import User, Listing, Bid


def index(request):
    listings = Listing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", context={
        "listings": listings,
    })


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    best_bid = Bid.objects.filter(listing=listing_id).order_by('value').last()
    return render(request, "auctions/listing_detail.html", context={
        "listing": listing,
        "bid": best_bid,
    })


@login_required(login_url="/login")
def add_listing(request):
    form = ListingForm()
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = Listing(
                user=User.objects.get(pk=request.user.id), title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                starting_price=form.cleaned_data["starting_price"],
                category=form.cleaned_data['category']
            )
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/add_listing.html", context={
        "form": form,
    })


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
