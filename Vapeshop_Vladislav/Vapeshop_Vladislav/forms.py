from django import forms
import datetime
from order.models import Order


class PriceOrderUpdate(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2)

class PriceOrderUpdate_2(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method']

class MonthForm(forms.Form):
    MONTH_CHOICES = [(i, (datetime.date(2000, i, 1).strftime('%B'))) for i in range(1, 13)]
    month = forms.ChoiceField(choices=MONTH_CHOICES, label='Выберите месяц')