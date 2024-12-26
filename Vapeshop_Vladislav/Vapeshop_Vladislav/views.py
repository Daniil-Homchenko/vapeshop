from calendar import month

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from goods.models import Goods
from order.models import Order, OrderItem, State
from .forms import PriceOrderUpdate, PriceOrderUpdate_2, PaymentForm, MonthForm
from .invoice import generate_invoice
import datetime
from django.db.models import Sum


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
    order = Order.objects.all().order_by(
        '-created_at'
    )
    order_items = OrderItem.objects.all()
    form = PriceOrderUpdate()
    form_2 = PriceOrderUpdate_2()
    form_3 = PaymentForm()
    context = {
        'orders': order,
        'order_items': order_items,
        'form': form,
        'form_2': form_2,
        'form_3': form_3,
    }
    return render(request, 'order_list.html', context=context)

def order_search(request):
    search = request.GET['search']
    orders = Order.objects.all()
    order_items = OrderItem.objects.all()
    form = PriceOrderUpdate()
    form_2 = PriceOrderUpdate_2()
    form_3 = PaymentForm()
    context = {
        'search': search,
        'orders': orders,
        'form': form,
        'form_2': form_2,
        'form_3': form_3,
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
    form_2 = PriceOrderUpdate_2()
    form_3 = PaymentForm()
    context = {
        'orders': order,
        'order_items': order_items,
        'form': form,
        'form_2': form_2,
        'form_3': form_3,
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

def update_payment_method(request, id):
    order = get_object_or_404(Order, id=id)
    form = PaymentForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        order.payment_method = cd['payment_method']
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


def sales_statistics(request):
    form = MonthForm(request.GET or None)
    selected_month = form.data.get('month', datetime.datetime.now().month)
    # Получение текущего года
    current_year = datetime.datetime.now().year
    # Фильтрация заказов по выбранному месяцу и текущему году
    orders = Order.objects.filter(created_at__year=current_year, created_at__month=selected_month, state__state__contains = get_object_or_404(State, id=2) )
    # Инициализация словаря для хранения суммы продаж по дням
    sales_by_day = {day: 0 for day in range(1, 32)}
    month_total = 0
    for order in orders:
        day = order.created_at.day
        sales_by_day[day] += order.total_price
        month_total += order.total_price
    context = { 'form': form,
                'sales_by_day': sales_by_day,
                'month_total': month_total,
                'current_year': current_year,
                'selected_month': int(selected_month),

                }
    return render(request, 'sales_statistics.html', context=context)

def orders_by_day(request, year, month, day):
    try:
        orders = get_list_or_404(Order, created_at__year=year, created_at__month=month, created_at__day=day)
        order_items = OrderItem.objects.all()
        context = { 'orders': orders,
                    'order_items': order_items,
                    'date': datetime.date(year, month, day)}
        return render(request, 'orders_by_day.html', context=context)
    except:
        return redirect('sales_statistics')