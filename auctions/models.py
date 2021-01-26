from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, null=False)
    description = models.CharField(max_length=512, blank=True, null=True)
    price = models.IntegerField(null = False, default= 1)
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

    def __str__(self):
        message = f"{self.title}, ${self.price}, Listed by {self.lister}"
        return message