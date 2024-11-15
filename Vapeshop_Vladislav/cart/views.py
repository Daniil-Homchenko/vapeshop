from itertools import product
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from goods import models
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.

def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(models.Goods, id=id)
    form = CartAddProductForm(request.POST, product_id=id)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)

def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(models.Goods, id=id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    lines = models.Line.objects.all().order_by('line')
    action = get_object_or_404(models.Categories, category__contains='Акции')
    categories_ = models.Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})

    return render(request, template_name='cart_detail.html', context={'cart': cart,
                                                                      'categories': categories,
                                                                      'lines': lines,})
