from django import forms

class PriceOrderUpdate(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2)

class PriceOrderUpdate_2(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2)