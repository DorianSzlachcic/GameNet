from django.forms import ModelForm
from .models import Rating, Game

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ["stars","description"]