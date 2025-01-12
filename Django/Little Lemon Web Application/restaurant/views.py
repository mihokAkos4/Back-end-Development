from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from django.core import serializers
from .models import Booking, MenuItem, Menu
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt

from .serializers import MenuItemSerializer, BookingSerializer, UserSerializer
from rest_framework import generics,viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer 

class BookingViewSet(viewsets.ModelViewSet):
   queryset =Booking.objects.all()
   serializer_class = BookingSerializer
   
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

def index(request):
    return render(request, 'index1.html', {})

def home(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def menu(request):
    menu_data = Menu.objects.all()
    main_data = {'menu': menu_data}
    
    return render(request, 'menu.html', {'menu': main_data})


def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''
        
    return render(request, 'menu_item.html', {'menu_item': menu_item})

def book(request):
    form = BookingForm()
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            
    context = {'form': form}
    return render(request, 'book.html', context)

def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    
    return render(request, 'bookings.html', {'bookings': booking_json})

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        
        if exist == False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')

    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')



class ListCreateView(APIView):
    def get(self, request):
        return Response({"message": "list of menu items"}, status.HTTP_200_OK)

    def post(self, request):
        return Response({"message": "new menu item created"}, status.HTTP_201_CREATED)


class SingleMenuItemView(APIView):
    def get(self, request, item_id):
        return Response({"message": f"Details of menu item {item_id}"}, status.HTTP_200_OK)

    def put(self, request, item_id):
        return Response({"message": f"Menu item {item_id} updated"}, status.HTTP_200_OK)

    def delete(self, request, item_id):
        return Response({"message": f"Menu item {item_id} deleted"}, status.HTTP_204_NO_CONTENT)




