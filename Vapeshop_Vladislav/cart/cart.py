from decimal import Decimal
from django.conf import settings
from goods.models import Goods
from django.shortcuts import get_object_or_404
from unicodedata import decimal


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        for item in cart:
            good = get_object_or_404(Goods, id=item)
            if cart[item]['quantity'] > good.quantity:
                cart[item]['quantity'] = int(good.quantity)
        self.cart = cart

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modifield = True

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        goods_ids = self.cart.keys()
        goods = Goods.objects.filter(id__in=goods_ids)
        for good in goods:
            self.cart[str(good.id)]['product'] = good
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    def get_len(self):
        return sum(item['quantity'] for item in self.cart.values())
    def get_total_price(self):
        return sum(float(item['price'])*float(item['quantity']) for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modifield =True