from datetime import datetime, timedelta
from django.utils import timezone
from lib2to3.fixes.fix_input import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from goods.models import Goods
from cart.cart import Cart
from order.models import Order, OrderItem, State
from .forms import PriceOrderUpdate, PriceOrderUpdate_2
from .invoice import generate_invoice


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('order_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')



@login_required
def order_list(request):
    today = timezone.now()
    start_date = today - timedelta(days=30)
    orders_date = Order.objects.filter(created_at__gte=start_date)
    mounth_sum = 0
    mounth_order = 0
    for item in orders_date:
        if item.state == get_object_or_404(State, id=2):
            mounth_sum += item.total_price
            mounth_order += 1
    start_date_2 = today - timedelta(days=7)
    orders_date_2 = Order.objects.filter(created_at__gte=start_date_2)
    week_sum = 0
    week_order = 0
    for item in orders_date_2:
        if item.state == get_object_or_404(State, id=2):
            week_sum += item.total_price
            week_order += 1
    start_date_3 = today - timedelta(days=1)
    orders_date_3 = Order.objects.filter(created_at__gte=start_date_3)
    daily_sum = 0
    daily_order = 0
    for item in orders_date_3:
        if item.state == get_object_or_404(State, id=2):
            daily_sum += item.total_price
            daily_order += 1
    order = Order.objects.all().order_by(
        '-created_at'
    )
    order_items = OrderItem.objects.all()
    form = PriceOrderUpdate()
    form_2 = PriceOrderUpdate_2()
    context = {
        'orders': order,
        'order_items': order_items,
        'form': form,
        'form_2': form_2,
        'mounth_sum':mounth_sum,
        'mounth_order': mounth_order,
        'week_sum': week_sum,
        'week_order': week_order,
        'daily_sum': daily_sum,
        'daily_order': daily_order
    }
    return render(request, 'order_list.html', context=context)

def order_search(request):
    search = request.GET['search']
    orders = Order.objects.all()
    order_items = OrderItem.objects.all()
    form = PriceOrderUpdate()
    context = {
        'search': search,
        'orders': orders,
        'form': form,
        'order_items': order_items,
    }
    return render(request, template_name='order_search.html', context=context)

@login_required
def order_completed(request):
    order = Order.objects.filter(state__state__contains = get_object_or_404(State, id=2)).order_by(
        '-created_at'
    )
    order_items = OrderItem.objects.all()
    context = {
        'orders': order,
        'order_items': order_items,
    }
    return render(request, 'order_comleted.html', context=context)

@login_required
def order_stoped(request):
    order = Order.objects.filter(state__state__contains = get_object_or_404(State, id=3)).order_by(
        '-created_at'
    )
    order_items = OrderItem.objects.all()
    context = {
        'orders': order,
        'order_items': order_items,
    }
    return render(request, 'order_stoped.html', context=context)

def order_reseted(request):
    order = Order.objects.filter(state__state__contains = get_object_or_404(State, id=1)).order_by(
        '-created_at'
    )
    order_items = OrderItem.objects.all()
    form = PriceOrderUpdate()
    context = {
        'orders': order,
        'order_items': order_items,
        'form': form,
    }
    return render(request, 'order_reseted.html', context=context)

def order_complete(request, id):
    order = get_object_or_404(Order, id=id)
    order_items = order.items.all()
    order.state = get_object_or_404(State, id=2)
    for order_item in order_items:
        good = get_object_or_404(Goods, id=order_item.product.id)
        good.quantity = int(good.quantity) - int(order_item.quantity)
        good.save()
    order.save()
    return redirect('order_list')

def get_invoice(request, id):
    order = get_object_or_404(Order, id=id)
    order_items = order.items.all()
    return redirect('order_list') and generate_invoice(order, order_items)

def order_stop(request, id):
    order = get_object_or_404(Order, id=id)
    order_items = order.items.all()
    if order.state == get_object_or_404(State, id=2):
        for order_item in order_items:
            good = get_object_or_404(Goods, id=order_item.product.id)
            good.quantity = int(good.quantity) + int(order_item.quantity)
            good.save()
    order.state = get_object_or_404(State, id=3)
    order.save()
    return redirect('order_list')

def order_reset(request, id):
    order = get_object_or_404(Order, id=id)
    order_items = order.items.all()
    if order.state == get_object_or_404(State, id=2):
        for order_item in order_items:
            good = get_object_or_404(Goods, id=order_item.product.id)
            good.quantity = int(good.quantity) + int(order_item.quantity)
            good.save()
    order.state = get_object_or_404(State, id=1)
    order.save()
    return redirect('order_list')

def update_total_price(request, id):
    order = get_object_or_404(Order, id=id)
    form = PriceOrderUpdate(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        order.total_price = cd['price']
        order.save()
    return redirect('order_list')

def update_price(request, order_id, order_item_id):
    order = get_object_or_404(Order, id=order_id)
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    form = PriceOrderUpdate_2(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        delta_price = (order_item.price - cd['price']) * order_item.quantity
        order_item.price = cd['price']
        order_item.save()
        order.total_price -= delta_price
        order.save()
    return redirect('order_list')