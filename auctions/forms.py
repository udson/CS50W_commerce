from django.forms import ModelForm
from .models import Listing


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category','starting_price',]
