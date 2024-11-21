"""
URL configuration for Vapeshop_Vladislav project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('order_list/', views.order_list, name='order_list'),
    path('update_total_price/<int:id>', views.update_total_price, name='update_total_price'),
    path('update_price/<int:order_id>/<order_item_id>', views.update_price, name='update_price'),
    path('order_complete/<int:id>', views.order_complete, name='order_complete'),
    path('get_invoice/<int:id>', views.get_invoice, name='get_invoice'),
    path('order_completed', views.order_completed, name='order_completed'),
    path('order_stop/<int:id>', views.order_stop, name='order_stop'),
    path('order_stoped', views.order_stoped, name='order_stoped'),
    path('order_reset/<int:id>', views.order_reset, name='order_reset'),
    path('order_reseted', views.order_reseted, name='order_reseted'),
    path('order_search', views.order_search, name='order_search'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('', include(('goods.urls', 'goods'), namespace='goods')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('order/', include(('order.urls', 'order'), namespace='order')),
]
