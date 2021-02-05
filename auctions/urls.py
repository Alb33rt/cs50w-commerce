from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("welcome", views.welcome, name="welcome"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("mywatchlist", views.watchlist, name="watchlist"),
    path("<int:auctionid>/addwatchlist", views.addtowatchlist, name="addwatchlist"),
    path("<int:auctionid>/removewatchlist", views.removefromwatchlist, name="removewatchlist"),
    path("<int:auctionid>/addcomment", views.addcomment, name="addcomment"),
    path("<int:auctionid>/placebid", views.placebid, name="placebid"),
    path("<int:auctionid>/closeauction", views.closeauction, name="closeauction"),
    path("<int:auctionid>/details", views.itemdetails, name="item"),
]
