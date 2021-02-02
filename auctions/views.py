from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Comment
from .forms import CommentForm

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    else:
        auctions = Auction.objects.exclude(active=False).all()
        return render(request, "auctions/index.html", {
            "listings": auctions
        })

@login_required(redirect_field_name='/login')
def create(request):
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

        # Saves the information of the auction into models object
        f = Auction(title=title, price=int(price), description=description, lister=current_user, active=True, image=image)
        f.save()
        
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html", {
                "Auction": Auction(),
                "category": Auction().get_choices()
            })


def item(request, name):

    # Getting auction id and comment filters
    auction = Auction.objects.get(title=name)
    auction_id = auction.id

    # Comment Function
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            current_user = request.user

            new_comment = Comment(comment=comment, poster=current_user)
            new_comment.save()

            # Associating the comment with current post
            new_comment.post.add(auction_id)


            # Getting the bunch of comments
            comments = Comment.objects.filter(post=auction_id).all()

            """Reminder here that it is impossible for comments to be false because the user has just posted a brand new one."""

            return render(request, 'auctions/item.html', {
                "auction": auction,
                "form": CommentForm(),
                "comments": comments,
            })

        else:
            pass

    if Comment.objects.filter(post=auction_id).all():
        comments = Comment.objects.filter(post=auction_id).all()
    else: 
        comments = False 
        
    return render(request, 'auctions/item.html', {
        "auction": auction,
        "form": CommentForm(),
        "comments": comments,
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


@login_required
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
