from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home, name="home"),
    path('about/', views.About, name="about"),
    path('menu/', views.Menu, name="menu"),
    path('book/', views.Booking, name="book"),
]