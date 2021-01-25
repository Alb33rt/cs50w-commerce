from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=32, null=False)
    description = models.CharField(max_length=512, null=True)
    price = models.IntegerField(null = False, default= 1)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")

    active = models.BooleanField(null=False)

    def __str__(self):
        message = f"{self.title}, ${self.price}, Listed by {self.lister}"
        return message