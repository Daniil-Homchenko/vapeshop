import hashlib
import time
from django.db import models
from django.db.models import CharField
from goods.models import Goods

# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=8, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    products = models.ManyToManyField(Goods, through='OrderItem')
    state = models.ForeignKey('State', default=1, related_name='order', verbose_name='Состояние', help_text='Укажите состояние заказа', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()[:8]
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.order_number)

class State(models.Model):
    state = CharField(max_length=15)
    def __str__(self):
        return str(self.state)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return str(self.order)