from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Comment, Bid, Watchlist
from .forms import CommentForm, BidForm

from .functions import get_highest_bid

import decimal

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("welcome"))
    else:
        user = request.user
        user_watching = user.watchlist.get()
        auctions = Auction.objects.exclude(active=False).all()
        watched_auctions = [val for val in auctions if val in user_watching.item.all()]
        return render(request, "auctions/index.html", {
            "listings": auctions,
            "watched_listings": watched_auctions,
        })

@login_required(redirect_field_name="/login")
def categorymenu(request):
    categories = [i[1] for i in Auction.CATEGORIES]
    return render(request, 'auctions/categorymenu.html', {
        "categories": categories,
    })

@login_required(redirect_field_name="/login")
def categorylist(request, category):
    categories = [i for i in Auction.CATEGORIES if i[1] == category]
    category_id = categories[0][0]
    category_name = categories[0][1]
    print(category_name)


    user = request.user
    user_watching = user.watchlist.get()

    auctions = Auction.objects.filter(category=category_id, active=True)
    watched_auctions = [val for val in auctions if val in user_watching.item.all()]

    return render(request, "auctions/categorylist.html", {
        "categoryname": category_name,
        "listings": auctions,
        "watched_listings": watched_auctions,
    })

@login_required(redirect_field_name='/login')
def createlisting(request):
    if request.method == "POST":
        # Define the basic information that is entered
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]

        image = request.POST.get('image', False)

        # Grabs the user information
        current_user = request.user

        message = False

        # Alert information for when the inserted information is in appropriate
        if title.strip() == '':
            message = "Please enter an appropriate title."
            return render(request, "auctions/create.html", {
                    "alert": message,
                    "Auction": Auction(),
                    "category": Auction().get_choices()
                })

        elif price.strip() == '':
            message = "Please enter a price that is appropriate."
            return render(request, "auctions/create.html", {
                    "alert": message,
                    "Auction": Auction(),
                    "category": Auction().get_choices()
                }) 

        title = title.strip()
        # Saves the information of the auction into models object
        f = Auction(title=title, price=int(price), description=description, lister=current_user, active=True, image=image)
        f.save()
        
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html", {
                "Auction": Auction(),
                "category": Auction().get_choices()
            })

@login_required(redirect_field_name='/login')
def itemdetails(request, auctionid):

    # Setting up all variables needed regardless of GET or POST
    auction = Auction.objects.filter(id=auctionid).get()

    # checks if item is being watched by the user
    user_watching = request.user.watchlist.get()
    watched = False
    if auction in user_watching.item.all():
        watched = True

    # Getting the current highest Bid 
    if Bid.objects.filter(post=auctionid):
        all_bids = Bid.objects.filter(post=auctionid).all()
                
        current_price = get_highest_bid(all_bids)
        current_bid = Bid.objects.filter(bid_price=current_price).get()
    else: 
        current_price = Auction.price
        current_bid = False

    if Comment.objects.filter(post=auctionid):
        comments = Comment.objects.filter(post=auctionid).all()
    else: 
        comments = False 
        
    return render(request, 'auctions/item.html', {
        "auction": auction,
        "form": CommentForm(),
        "comments": comments,
        "bid": current_bid,
        "bidForm": BidForm(),
        "watched": watched,
    })

@login_required(redirect_field_name='/login')
def addcomment(request, auctionid):
    commentform = CommentForm(request.POST)
    if commentform.is_valid():
        comment = commentform.cleaned_data['comment']
        current_user = request.user

        comment = comment.strip()
        new_comment = Comment(comment=comment, poster=current_user)
        new_comment.save()

        # Associating the comment with current post
        new_comment.post.add(auctionid)

        """Reminder here that it is impossible for comments to be false because the user has just posted a brand new one."""

        return HttpResponseRedirect(reverse('item', args=[auctionid]))

@login_required(redirect_field_name='/login')
def addtowatchlist(request, auctionid):
    auction = Auction.objects.filter(id=auctionid)
    if Watchlist.objects.filter(user=request.user, item=auctionid):
        message="You already have this item in your watchlist"
        return HttpResponseRedirect(reverse('index'))

    user = request.user
    (users_list, created) = user.watchlist.get_or_create(user=user)
    users_list.item.add(auctionid)
  
    return HttpResponseRedirect(reverse('index'))

@login_required(redirect_field_name='/login')
def removefromwatchlist(request, auctionid):
    auction = Auction.objects.filter(id=auctionid)

    user = request.user
    users_list = user.watchlist.get(user=user)
    users_list.item.remove(auctionid)

    return HttpResponseRedirect(reverse('watchlist'))

@login_required(redirect_field_name='/login')
def watchlist(request):
    user = request.user
    users_list, created = user.watchlist.get_or_create()
   
    # Uses list basic search method
    matches = [val for val in Auction.objects.all() if val in users_list.item.all()]

    return render(request, 'auctions/watchlist.html', {
        "listings": matches,
    })

@login_required(redirect_field_name='/login')
def placebid(request, auctionid):   

    # Sets up variables for use
    auction = Auction.objects.filter(id=auctionid).get()
    if Bid.objects.filter(post=auctionid):
        all_bids = Bid.objects.filter(post=auctionid).all()
                
        current_price = get_highest_bid(all_bids)
        current_bid = Bid.objects.filter(bid_price=current_price).get()
    else: 
        current_price = auction.price
        current_bid = False

    # get the potential forms submitted
    bid_form = BidForm(request.POST)

    # When the bid form is being submitted
    if bid_form.is_valid():
        bidder = request.user
        bid_price = bid_form.cleaned_data['bid_price']

        if bid_price > decimal.Decimal(current_price):
            bid = Bid(bidder=bidder, bid_price=bid_price, post=auction)
            bid.save()

            return HttpResponseRedirect(reverse('item', args=[auctionid]))

        else:
            message= "Please bid higher than the current highest bid, please re-enter your bid."

            # Gets if the item is being watched
            user_watching = request.user.watchlist.get()
            watched = False
            if auction in user_watching.item.all():
                watched = True

            if Comment.objects.filter(post=auctionid):
                comments = Comment.objects.filter(post=auctionid).all()
            else: 
                comments = False 


            return render(request, 'auctions/item.html', {
                "message": message,
                "auction": auction,
                "form": CommentForm(),
                "comments": comments,
                "bid": current_bid,
                "bidForm": BidForm(),
                "watched": watched,
            })

def closeauction(request, auctionid):
    auction = Auction.objects.get(id=auctionid)
    if auction.active == True:
        auction.active = False
        auction.save()
        return HttpResponseRedirect(reverse('index'))
    
    else:
        return HttpResponseRedirect(reverse('item'))


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


@login_required(redirect_field_name='/login')
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
            users_list = Watchlist(user=user)
            users_list.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def welcome(request):
    return render(request, "auctions/welcome.html")