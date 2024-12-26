from django.contrib import admin
from .models import Order, OrderItem, State, Payment_method
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(State)
admin.site.register(Payment_method)