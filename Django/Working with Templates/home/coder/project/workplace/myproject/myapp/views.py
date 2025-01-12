from django.shortcuts import render

# Create your views here for Home, Menu, About and Booking

def Home(request):
    return render(request, 'index.html')

def Menu(request):
    return render(request, 'menu.html')

def About(request):
    return render(request, 'about.html')

def Booking(request):
    return render(request, 'book.html')
