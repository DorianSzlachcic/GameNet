from distutils.command.upload import upload
from click import edit
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length=128, help_text="Tytuł gry")
    developer = models.CharField(max_length=128, help_text="Developer")
    description = models.TextField(max_length=512, help_text="Opis gry")
    release_date = models.DateField(null=True, blank=True, help_text="Data wydania gry")
    image = models.ImageField(upload_to="uploads/", blank=True)
    image_link = models.CharField(max_length=512, help_text="Link do zdjęcia", null=True, blank=True)
    trailer = models.CharField(max_length=512, help_text="Link do trailera gry", null=True, blank=True)

    def __str__(self) -> str:
        return self.title + " - " + self.developer

class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(max_length=256, help_text="Twoja opinia", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.author.username + " - " + self.game.title