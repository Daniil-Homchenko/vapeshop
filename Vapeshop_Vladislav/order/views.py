from django.utils import timezone
from itertools import product
from lib2to3.fixes.fix_input import context
from venv import create

from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from goods.models import Goods, Categories, Line
from .models import Order, OrderItem, State

# Create your views here.
def checkout(request):
    cart = Cart(request)
    order = Order.objects.create(created_at = timezone.now())
    total_price = 0
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=Goods.objects.get(pk=item['product'].id),
            quantity=item['quantity'],
            price=Goods.objects.get(pk=item['product'].id).price
        )
        total_price += Goods.objects.get(pk=item['product'].id).price * item['quantity']
    order.total_price = total_price
    order.save()
    cart.clear()  # Очистка корзины после оформления заказа
    cart = Cart(request)
    order_items = OrderItem.objects.all()
    categories = Categories.objects.all()
    context = {
        'cart': cart,
        'categories': categories,
        'order':order,
        'order_items':order_items,
    }
    return render(request, 'order_successfull.html', context=context)