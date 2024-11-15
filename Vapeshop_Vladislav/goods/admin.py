from django.contrib import admin
from .models import Goods, Categories, Line


# Register your models here.
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('taste', 'line', 'stronghold', 'category',  'price', 'quantity') # Какие поля отображать в списке
    ordering = ('line__line',)
    def get_line_line(self, obj):
        return obj.line.line
    get_line_line.admin_order_field = 'line__line'  # Позволяет сортировать по полю
    get_line_line.short_description = 'Line Line'
class LineAdmin(admin.ModelAdmin):
    ordering = ('line',)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Categories)
admin.site.register(Line, LineAdmin)
