from django.urls import path
from reviews import views

urlpatterns = [
    path("your_reviews/", views.your_reviews, name="yourReviews"),
    path("add/", views.add, name='addReviews'),
    path("delete/<id>/", views.delete, name='deleteReviews'),
    path("edit/<id>/", views.edit, name='editReviews'),
    path("<id>/", views.reviews_site, name="review"),
    path("",views.reviews_list, name="reviewsList")
]