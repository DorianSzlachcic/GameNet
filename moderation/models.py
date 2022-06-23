from django.db import models
from games.models import Rating

# Create your models here.

class ModerationMessage(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)