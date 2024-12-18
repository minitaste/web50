from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "categories": categories,
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


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    is_in_watchlist = listing in request.user.watchlist.all() if request.user.is_authenticated else False

    if request.method == "POST":
        user = request.user
        if is_in_watchlist:
            user.watchlist.remove(listing)
            messages.info(request, "Listing removed from watchlist.")
        else:
            user.watchlist.add(listing)
            messages.info(request, "Listing added to watchlist.")
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    comments = listing.comment_set.all().order_by('-created')
    
    return render(request, "auctions/listing.html", {
        "listing": listing, 
        "is_in_watchlist": is_in_watchlist,
        "comments": comments,
    })
    
@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        
        try:
            bid = int(request.POST["bid"])
        except ValueError:
            messages.error(request, "Enter a valid number.")
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

        highest_bid = listing.get_highest_bid()  
        highest_amount = highest_bid.amount if highest_bid else listing.price  

        if bid > highest_amount:
            Bid.objects.create(user=request.user, listing=listing, amount=bid)
            messages.success(request, "Your bid was placed successfully!")
        else:
            messages.error(request, "Bid must be higher than the current price.")
        
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    

def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        comment = request.POST["comment"]
        Comment.objects.create(user=request.user, listing=listing, description=comment)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    return render(request, "auctions/listing.html")


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        price = request.POST["price"]
        category = request.POST["category"]
        description = request.POST["description"]
        img_url = request.POST.get("img_url", "")

        if not title or not price or not category or not description:
            return render(request, "auctions/create.html", {
                "error": "Усі поля обов’язкові для заповнення."
            })

        try:
            price = int(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            return render(request, "auctions/create.html", {
                "error": "Ціна повинна бути позитивним числом."
            })
        
        listing = Listing(
            owner=request.user,  
            title=title,
            price=price,
            category=category,
            description=description,
            img_url=img_url
        )
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    return render(request, "auctions/create.html")


def categories(request):
    if request.method == "POST":
        category = request.POST["category"]  
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/categories.html", {
            "listings": listings,
            "category": category,
        })
    else:
        categories = Listing.objects.values_list('category', flat=True).distinct()
        return render(request, "auctions/categories.html", {
            "categories": categories,
        })
    

def watchlist(request):
    if request.user.is_authenticated:
        user = request.user
        listings = user.watchlist.all()
     
        return render(request, "auctions/watchlist.html", {
            "listings": listings
        })
    return render(request, "auctions/watchlist.html")