from django.contrib import admin
from django.urls import path
from BookListAPI import views
from django.urls import include

urlpatterns = [
    path("admin", admin.site.urls),
    path("books", views.books),
    path('api/', include('BookListAPI.urls')),
]