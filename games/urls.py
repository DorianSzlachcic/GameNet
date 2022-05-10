from django.urls import path
from games import views

urlpatterns = [
    path("<id>/", views.game_site, name="game")
]