from .models import Booking
from django import forms

class BookingForm(forms.ModelForm):
    class Meta:
        Model = Booking
        Field = "__all__"