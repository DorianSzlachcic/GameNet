from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField

# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length=128, help_text="Tytuł gry")
    developer = models.CharField(max_length=128, help_text="Developer")
    description = models.TextField(max_length=1024, help_text="Opis gry")
    release_date = models.DateField(null=True, blank=True, help_text="Data wydania gry")
    image = CloudinaryField("game_image", null=True, blank=True)
    image_link = models.CharField(max_length=512, help_text="Link do zdjęcia", null=True, blank=True)
    trailer = models.CharField(max_length=512, help_text="Link do trailera gry", null=True, blank=True)

    def __str__(self) -> str:
        return self.title + " - " + self.developer

class Rating(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(max_length=512, help_text="Twoja opinia", null=True, blank=True)
    accepted = models.BooleanField(null=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.game.title