from django.forms import ModelForm
from .models import Auction, Comment

# Defining the forms for the object
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']