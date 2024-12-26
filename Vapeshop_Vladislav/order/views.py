from django.utils import timezone
from itertools import product
from lib2to3.fixes.fix_input import context
from venv import create

from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from goods.models import Goods, Categories, Line
from .models import Order, OrderItem, Payment_method


# Create your views here.
def checkout(request):
    cart = Cart(request)
    payment = get_object_or_404(Payment_method, id=1)
    if cart:
        order = Order.objects.create(created_at = timezone.now().date(), payment_method=payment)
        total_price = 0
        for item in cart:
            good = Goods.objects.get(pk=item['product'].id)
            if item['quantity'] > good.quantity:
                OrderItem.objects.create(
                    order=order,
                    product=good,
                    quantity=good.quantity,
                    price=good.price
                )
                total_price += good.price * good.quantity
            else:
                OrderItem.objects.create(
                    order=order,
                    product=good,
                    quantity=item['quantity'],
                    price=good.price
                )
                total_price += good.price * item['quantity']
        order.total_price = total_price
        order.save()
        cart.clear()  # Очистка корзины после оформления заказа
        cart = Cart(request)
        order_items = OrderItem.objects.all()
        action = get_object_or_404(Categories, category__contains='Акции')
        categories_ = Categories.objects.exclude(id=action.id).order_by('category')
        categories = [action] + list(categories_)
        context = {
            'cart': cart,
            'categories': categories,
            'order':order,
            'order_items':order_items,
        }
        return render(request, 'order_successfull.html', context=context)
    else:
        return redirect('cart:cart_detail')