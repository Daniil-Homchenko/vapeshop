from email.policy import default
from django import forms
from django.shortcuts import get_object_or_404
from order.models import Order

class PriceOrderUpdate(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2)