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