from django.db import models
from django.contrib.auth.models import User
from games.models import Game
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Review(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    points = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    lead = models.TextField(max_length=1024, default="Zapowiedź")
    image = CloudinaryField("review_image", null=True, blank=True)
    content = RichTextField()
    summary = models.TextField(max_length=1024, default="Podsumowanie")
    created_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)