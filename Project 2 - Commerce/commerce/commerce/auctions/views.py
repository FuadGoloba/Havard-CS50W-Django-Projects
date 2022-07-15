from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import User, AuctionListing, Bid, Comment, Category, AuctionStatus, Watchlist


def index(request):
    # Filter all listings that are open/active
    listing = AuctionListing.objects.filter(status= 1).order_by('-listing_date')
    return render(request, "auctions/index.html", {
        "listings" : listing
    })

@login_required(login_url='/login')
def create_listing(request):
    default_image = "https://th.bing.com/th/id/OIP.MiyTaoyL4bgDzZSGG9-oaAHaHa?w=170&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7"
    if request.POST:
        title = request.POST["title"]
        description = request.POST["description"]
        listing_price = request.POST["listing_price"]
        image = default_image if not request.POST["image"] else request.POST["image"]
        category = Category.objects.get(pk=int(request.POST["category"]))
        seller = User.objects.get(pk=int(request.user.id))
        status = AuctionStatus.objects.get(pk=1)

        # Create Listing and save
        try:
            listing = AuctionListing(title=title, description=description, listing_price=listing_price, image=image, category=category, seller=seller, status=status) # Create a new listing
            listing.save() # Persist the Listing
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "auctions/createlisting.html", {
                "message": "Listing already exists"
            })
    return render(request, "auctions/createlisting.html", {
        "categories": Category.objects.all()
    })


def category_listing(request, category_id):
    # Get all active listings for a category
    listings = AuctionListing.objects.filter(Q(category=category_id) & Q(status=1)).order_by('-listing_date')
    return render(request, "auctions/categorylisting.html", {
        "listings" : listings
    })

def closed_listing(request):
    # Get all listings that have been closed
    listing = AuctionListing.objects.filter(status=2).order_by('-listing_date')
    return render(request, "auctions/closedlisting.html", {
        "listings" : listing
    })

def item_detail(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id) # Get the listing selected by the user
    comments = Comment.objects.filter(listing=listing_id).order_by('-comment_date') # Get user's comment
    user = request.user if request.user.is_authenticated else None # make user object none for unsigned users
    biddings = listing.biddings.all() # Get all biddings on a listing 
    
    # Query to get items in a user's watchlist if it exists 
    try:
        watchlist = Watchlist.objects.get(Q(user=user) & Q(listing=listing))
    except Watchlist.DoesNotExist:
        watchlist = None

    # Query to get the latest bid on a listing if it exists
    try:
        latest_bid = Bid.objects.filter(listing=listing_id).latest('bid_date')
    except Bid.DoesNotExist:
        latest_bid = None

    if request.POST:
        # Check that user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        
        # Get user's bid and create a new bid
        user_bid = int(request.POST["bid"]) 
        if (latest_bid is not None and user_bid > latest_bid.bid_price) or (latest_bid is None and user_bid >= listing.listing_price):
            new_bid = Bid(bidder=User.objects.get(pk=int(request.user.id)), bid_price=user_bid, listing=listing) # Create a new bid
            new_bid.save() #save bid in model
            return HttpResponseRedirect(reverse("index"))

        return render(request, "auctions/item_detail.html", {
            "message": "Your bid must be higher than the latest bid",
            "listing" : listing,
            "latest_bid" : latest_bid,
            "comments" : comments,
            "watchlist" : watchlist,
            "biddings" : biddings
        })       
    return render(request, "auctions/item_detail.html", {
        "listing" : listing,
        "latest_bid" : latest_bid,
        "comments" : comments,
        "watchlist" : watchlist,
        "biddings" : biddings
    })

@login_required(login_url='/login')
def add_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    added = Watchlist(user=request.user, listing=listing) # Add listing to User's watchlist model
    added.save() # save listing to user's watchlist
    return HttpResponseRedirect(reverse("item_detail", args=[listing_id]))

def remove_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    Watchlist.objects.get(Q(user=request.user) & Q(listing=listing)).delete() # Delete listing from user's watchlist
    return HttpResponseRedirect(reverse("item_detail", args=[listing_id]))

@login_required(login_url='/login')
def add_comment(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    if request.POST:
        user_comment = request.POST["comment"]
        if user_comment:
            new_comment = Comment(comment=user_comment, reviewer=request.user, listing=listing)
            new_comment.save()
    return HttpResponseRedirect(reverse("item_detail", args=[listing_id]))

def close_bid(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    if request.POST["close"]:
        # Update listing status to closed if seller chooses to close auction
        listing.status = AuctionStatus.objects.get(pk=2)
        listing.save(update_fields=['status'])
    return HttpResponseRedirect(reverse("item_detail", args=[listing_id]))

def view_watchlist(request):
    # Get all items in a user's watchlist
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist" : watchlist
    })

def categories(request):
    # Display all Categories
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : all_categories
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

