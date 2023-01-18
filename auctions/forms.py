from django import forms
from .models import Listing

custom = {'class': 'form-control'}

class ListingForm(forms.ModelForm):
    template_name = 'bootstrap_form_snippet.html'

    class Meta:
        model = Listing
        fields = ['title', 'description', 'image', 'category','starting_price',]
        widgets = {
            'title': forms.TextInput(attrs=custom),
            'description': forms.Textarea(attrs=custom),
            'category': forms.Select(attrs=custom),
            'image': forms.URLInput(attrs=custom),
            'starting_price': forms.NumberInput(attrs=custom),
        }
