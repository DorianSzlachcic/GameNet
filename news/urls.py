from django.urls import path
from news import views

urlpatterns = [
    path("your_news/", views.your_news, name="yourNews"),
    path("add/", views.add, name='addNews'),
    path("delete/<id>/", views.delete, name='deleteNews'),
    path("edit/<id>/", views.edit, name='editNews'),
    path("<id>/", views.news_site, name="news"),
    path("",views.news_list, name="newsList")
]