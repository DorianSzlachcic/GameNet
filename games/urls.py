from django.urls import path
from games import views

urlpatterns = [
    path("ranking/", views.ranking, name="ranking"),
    path("list/", views.game_list, name="gameList"),
    path("<id>/", views.game_site, name="game"),
    path("delete/<id>", views.deleteRating, name="deleteRating"),
    path("edit/<id>", views.editRating, name="editRating"),
    path("", views.search, name="search")
]