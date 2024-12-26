from django import forms
from goods.models import Goods
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 1000)]

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField( initial='1', widget=forms.NumberInput(attrs={
            'class': 'custom-select',
            'id': 'valueInput',
        }))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        try:
            quantity = int(quantity)
        except ValueError:
            raise forms.ValidationError("Введите целое число.")
        return quantity