from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime


class User(AbstractUser):
    pass

class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, null=False)
    description = models.TextField(max_length=512, blank=True, null=True)
    price = models.DecimalField(null = False, default= 1, max_digits=10, decimal_places=2)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister") 

    # Defines the choices of category the object can be become
    LIFE = "LF"
    SCHOOL = "SC"
    TECH = "TE"
    PROFESSIONAL = "PR"
    CATEGORIES = [
            (LIFE, 'Life'),
            (SCHOOL, 'School'),
            (TECH, "Tech"),
            (PROFESSIONAL, 'Professional'),
        ]
    category = models.CharField(choices=CATEGORIES, default=LIFE, max_length=16)

    image = models.ImageField(upload_to="images/", blank=True, null=True)
    active = models.BooleanField(null=False)

    # Time related variables
    listed_time = models.DateTimeField(auto_now_add=True)

    def     __str__(self):
        message = f"{self.title}, ${self.price}, Listed by {self.lister}"
        return message

    def get_choices(self):
        lst = []
        choices = self.CATEGORIES
        for choiceid in choices:
            lst.append(choiceid[1])

        return lst

    def category_string(self):
        categorization = self.category

        return f"Category: {categorization}"    

class Comment(models.Model): 
    comment = models.TextField(max_length=1024, blank=False)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    time = models.DateTimeField(auto_now_add=True)

    # Commenting on Post
    post = models.ManyToManyField(Auction)

    def __str__(self):
        message = f"Comment by {self.poster}"
        return message

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_price = models.DecimalField(decimal_places=2, max_digits=10)

    post = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction")

    def __str__(self):
        message = f"Bid by {self.bidder} with {self.bid_price} on the line"
        return message
