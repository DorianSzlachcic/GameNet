from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('accounts.urls')),
    path('games/',include('games.urls')),
    path('news/',include('news.urls')),
    path('reviews/',include('reviews.urls')),
    path('moderation/',include('moderation.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls)
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)