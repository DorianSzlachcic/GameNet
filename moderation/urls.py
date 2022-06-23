from django.urls import path
from moderation import views

urlpatterns = [
    path("", views.moderator_panel, name="moderatorPanel"),
    path("accept/<id>/", views.accept, name="acceptRating"),
    path("reject/<id>/", views.reject, name="rejectRating")
]