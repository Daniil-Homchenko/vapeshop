from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .models import Goods, Categories, Line


# Create your views here.



def goods_list(request):
    cart = Cart(request)
    lines = Line.objects.all().order_by('brand')
    goods_list = {}
    for line in lines:
        goods_list[line] = Goods.objects.filter(line=line).order_by('taste')[:8]
    action = get_object_or_404(Categories, category__contains='Акции')
    categories_ = Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    cart_product_form = CartAddProductForm
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    cart_ids= [int(i) for i in cart.cart.keys()]
    context = {
        'goods_list': goods_list,
        'cart' : cart,
        'categories': categories,
        'lines': lines,
        'cart_product_form': cart_product_form,
        'cart_ids': cart_ids
    }

    return render(request, template_name='goods_index.html', context=context)


def goods_detail(request, pk, line_id):
    cart = Cart(request)
    good = Goods.objects.get(pk=pk)
    line_1 = Line.objects.get(id=line_id)
    lines = Line.objects.all().order_by('brand')
    action = get_object_or_404(Categories, category__contains='Акции')
    categories_ = Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    goods_also = Goods.objects.filter(
        line=line_1
    ).exclude(id=good.id).order_by(
        'taste'
    )[:8]
    goods_list = {}
    for line in lines:
        goods_list[line] = Goods.objects.filter(line=line).order_by('taste')[:1]
    cart_product_form = CartAddProductForm
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    cart_ids = [int(i) for i in cart.cart.keys()]
    context = {'good': good,
               'goods_list': goods_list,
               'goods_also': goods_also,
               'cart' : cart,
               'lines': lines,
               'line': line_1,
               'cart_product_form': cart_product_form,
               'categories': categories,
               'cart_ids': cart_ids
    }
    return render(request, 'goods_detail.html', context=context)

def goods_search(request):
    cart = Cart(request)
    goods = Goods.objects.all().order_by(
        'taste'
    )
    search = request.GET['search']
    lines = Line.objects.all().order_by('brand')
    goods_list = {}
    for line in lines:
        goods_list[line] = Goods.objects.filter(line=line).order_by('taste')[:1]
    action = get_object_or_404(Categories, category__contains='Акции')
    categories_ = Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    cart_product_form = CartAddProductForm
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    cart_ids = [int(i) for i in cart.cart.keys()]
    context = {
        'goods': goods,
        'goods_list': goods_list,
        'search': search,
        'cart': cart,
        'categories': categories,
        'lines': lines,
        'cart_product_form': cart_product_form,
        'cart_ids': cart_ids
    }
    return render(request, template_name='goods_search.html', context=context)

def goods_category(request, category_id):
    cart = Cart(request)
    category = get_object_or_404(Categories, id=category_id)
    lines = Line.objects.all().order_by('brand')
    goods_list = {}
    goods_list_1 = {}
    for line in lines:
        goods_list[line] = Goods.objects.filter(line=line).order_by('taste')[:1]
        goods_list_1[line] = Goods.objects.filter(line=line, category__category__contains=category).order_by('taste')[:8]
    action = get_object_or_404(Categories, category__contains='Акции')
    categories_ = Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    cart_product_form = CartAddProductForm
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    cart_ids = [int(i) for i in cart.cart.keys()]
    context = {
        'categories': categories,
        'lines': lines,
        'cart': cart,
        "category": category,
        "goods_list": goods_list,
        "goods_list_1": goods_list_1,
        'cart_product_form': cart_product_form,
        'cart_ids': cart_ids
    }
    return render(request, template_name="goods_category.html", context=context)

def goods_line(request, line_id):
    cart = Cart(request)
    line = get_object_or_404(Line, id=line_id)
    goods_line = Goods.objects.filter(
        line=line
    ).order_by(
        'taste'
    )
    lines = Line.objects.all().order_by('brand')
    goods_list = {}
    for linee in lines:
        goods_list[linee] = Goods.objects.filter(line=linee).order_by('taste')[:1]
    action = get_object_or_404(Categories, category__contains='Акции')
    categories_ = Categories.objects.exclude(id=action.id).order_by('category')
    categories = [action] + list(categories_)
    cart_product_form = CartAddProductForm
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    cart_ids = [int(i) for i in cart.cart.keys()]
    context = {
        'categories': categories,
        'lines': lines,
        'cart': cart,
        "line": line,
        "goods_line": goods_line,
        "goods_list": goods_list,
        'cart_product_form': cart_product_form,
        'cart_ids': cart_ids
    }
    return render(request, template_name="goods_line.html", context=context)