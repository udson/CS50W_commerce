from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import ListingForm
from .models import *


def index(request):
    listings = Listing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", context={
        "listings": listings,
    })


def listing_detail(request, listing_id):
    context = {}
    user = request.user
    listing = get_object_or_404(Listing, pk=listing_id)
    best_bid = Bid.objects.filter(listing=listing_id).order_by('value').last()

    if request.method == "POST":
        if user.is_authenticated:
            try:
                bid = float(request.POST["bid"])
                best_bid_value = listing.starting_price

                if best_bid is not None:
                    best_bid_value = best_bid.value
                
                if bid > best_bid_value:
                    new_bid = Bid(
                        user=User.objects.get(pk=request.user.id),
                        listing=listing,
                        value=bid
                    )
                    new_bid.save()
                    best_bid = new_bid
                else:
                    context["bid_error"] = f"Place a bid greater than ${best_bid_value}."
            except ValueError:
                context["bid_error"] = "This field is required." if request.POST["bid"] == "" else "Enter a number."
        else:
            context["bid_error"] = "Login to place a bid."

    context["listing"] = listing
    context["best_bid"] = best_bid

    return render(request, "auctions/listing_detail.html", context=context)


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
                category=form.cleaned_data["category"],
                image=form.cleaned_data["image"]
            )
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/add_listing.html", context={
        "form": form,
    })


@login_required(login_url="/login")
def close_listing(request, listing_id):
    user = User.objects.get(pk=request.user.id)
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.user == user:
        listing.is_active = False
        listing.save()
    
    return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))


@login_required(login_url="/login")
def watchlist(request):
    user = User.objects.get(pk=request.user.id)

    return render(request, "auctions/index.html", context={
        "page_heading": "My Watchlist",
        "listings":user.watchlist.all(),
    })


@login_required(login_url="/login")
def watchlist_add_item(request, listing_id):
    user = User.objects.get(pk=request.user.id)
    user.watchlist.add(get_object_or_404(Listing, pk=listing_id))
    return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))


@login_required(login_url="/login")
def watchlist_remove_item(request, listing_id):
    user = User.objects.get(pk=request.user.id)
    user.watchlist.remove(get_object_or_404(Listing, pk=listing_id))
    return HttpResponseRedirect(reverse("listing_detail", args=[listing_id]))


def categories(request):
    return render(request, "auctions/categories.html", context={
        "categories": Category.objects.all(),
    })

def category(request, category):
    
    return render(request, "auctions/index.html", context={
        "page_heading": f"Category: {get_object_or_404(Category, pk=category)}",
        "listings": Listing.objects.filter(category__pk=category, is_active=True),
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
