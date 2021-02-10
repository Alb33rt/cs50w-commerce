from django import forms
from django.forms import ModelForm
from .models import Auction, Comment, Bid

# Defining the forms for the object
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_price']
        widgets = {
            'bid_price': forms.NumberInput(attrs={'class': 'form-control  mb-4'})
        }

class CreateForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'price', 'category', 'image']
    
    def __init__(self, *args, **kwargs):
        # inherit data from superclass ModelForm
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'type': 'textarea', 'class': 'form-control', 'rows': 6, 'cols': 40, 'placeholder': "Enter Basic Information"})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})