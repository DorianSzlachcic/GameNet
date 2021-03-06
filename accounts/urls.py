from django.urls import path
from . import views

urlpatterns = [
    path('',views.homePage ,name='home'),
    path('login/',views.loginPage ,name='login'),
    path('logout/',views.logoutUser ,name='logout'),
    path('register/',views.registerPage ,name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('my_profile/',views.profilePage, name='profile'),
    path('delete_account/', views.deleteAccount, name='deleteAccount'),
    path('change_password/', views.change_password, name='changePassword')
]