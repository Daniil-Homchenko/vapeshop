from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .models import Goods, Categories, Line


# Create your views here.



def goods_list(request):
    cart = Cart(request)
    goods = Goods.objects.all()
    lines = Line.objects.all().order_by('line')
    action = get_object_or_404(Categories, category__contains='Акции')
    categories_ = Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    cart_product_form = CartAddProductForm
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    cart_ids= [int(i) for i in cart.cart.keys()]
    context = {
        'action':action,
        'goods': goods,
        'cart' : cart,
        'categories': categories,
        'lines': lines,
        'cart_product_form': cart_product_form,
        'cart_ids': cart_ids
    }

    return render(request, template_name='goods_index.html', context=context)


def goods_detail(request, pk, category):
    cart = Cart(request)
    good = Goods.objects.get(pk=pk)
    lines = Line.objects.all().order_by('line')
    action = get_object_or_404(Categories, category__contains='Акции')
    categories_ = Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    goods = Goods.objects.filter(
        category__category__contains=category
    ).order_by(
        '-created_on')
    cart_product_form = CartAddProductForm
    context = {'good': good,
               'goods': goods,
               'cart' : cart,
               'lines': lines,
               'cart_product_form': cart_product_form,
               'categories': categories,
    }
    return render(request, 'goods_detail.html', context=context)

def goods_search(request):
    cart = Cart(request)
    goods = Goods.objects.all()
    search = request.GET['search']
    cart_product_form = CartAddProductForm
    lines = Line.objects.all().order_by('line')
    action = get_object_or_404(Categories, category__contains='Акции')
    categories_ = Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    context = {
        'goods': goods,
        'search': search,
        'cart': cart,
        'categories': categories,
        'lines': lines,
        'cart_product_form': cart_product_form
    }
    return render(request, template_name='goods_search.html', context=context)

def goods_category(request, category):
    cart = Cart(request)
    goods = Goods.objects.filter(
        category__category__contains=category
    ).order_by(
        '-created_on'
    )
    lines = Line.objects.all().order_by('line')
    action = get_object_or_404(Categories, category__contains='Акции')
    categories_ = Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    context = {
        'categories': categories,
        'lines': lines,
        'cart': cart,
        "category": category,
        "goods": goods
    }
    return render(request, template_name="goods_category.html", context=context)

def goods_line(request, line):
    cart = Cart(request)
    goods = Goods.objects.filter(
        line__line__contains=line
    ).order_by(
        '-created_on'
    )
    lines = Line.objects.all().order_by('line')
    categories = Categories.objects.all()
    context = {
        'categories': categories,
        'lines': lines,
        'cart': cart,
        "line": line,
        "goods": goods
    }
    return render(request, template_name="goods_line.html", context=context)