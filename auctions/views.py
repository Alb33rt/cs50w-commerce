from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Comment, Bid
from .forms import CommentForm, BidForm

from .functions import get_highest_bid

import decimal

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("welcome"))
    else:
        auctions = Auction.objects.exclude(active=False).all()
        return render(request, "auctions/index.html", {
            "listings": auctions
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