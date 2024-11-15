from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.goods_list, name='goods_list'),
    path('<int:pk>/<category>', views.goods_detail, name='goods_detail'),
    path('search/', views.goods_search, name='goods_search'),
    path('"<category>"/', views.goods_category, name='goods_category'),
    path('"<line>"', views.goods_line, name='goods_line')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)