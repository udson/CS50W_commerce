from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categorie(models.Model):
    name = models.CharField(unique=True)

    def __str__(self) -> str:
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    title = models.CharField()
    description = models.TextField()
    starting_price = models.DecimalField(decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Bid(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    listing = models.ForeignKey(to=Listing, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(decimal_places=2)

    def __str__(self) -> str:
        return f"{self.value} on {self.listing} by {self.user}"