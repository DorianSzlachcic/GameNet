from django.urls import path
from games import views

urlpatterns = [
    path("<id>/", views.game_site, name="game"),
    path("delete/<id>", views.deleteRating, name="deleteRating"),
    path("edit/<id>", views.editRating, name="editRating")
]