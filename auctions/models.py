from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Listing(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, blank=True, null=True)
    starting_price = models.DecimalField(max_digits=20, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Bid(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    listing = models.ForeignKey(to=Listing, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.value} on {self.listing} by {self.user}"