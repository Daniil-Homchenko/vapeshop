from django.db import models


# Create your models here.
class Goods(models.Model):
    taste = models.CharField(max_length=100, verbose_name='Вкус/модель товара', help_text='Укажите вкус или модель товара', null=True, blank=True)
    description = models.TextField(verbose_name="Описание товара", help_text="Введите описание товара", null=True, blank=True)
    tegs = models.TextField(verbose_name="Теги товара", help_text="Введите теги для поиска товара", null=True, blank=True)
    category = models.ForeignKey('Categories', related_name='goods', verbose_name='Категория',
                                          help_text='Укажите категорию товара', on_delete=models.CASCADE, null=True, blank=True)
    line = models.ForeignKey('Line', related_name='goods', verbose_name='Линейка',
                                          help_text='Укажите линейку товара', on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='images/', verbose_name='Изображение товара', help_text='Выберите изображение товара', null=True, blank=True)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=8, verbose_name="Цена",
                                help_text="Укажите цену товара")
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quantity = models.DecimalField(default=0, decimal_places=0, max_digits=8, verbose_name="Количество товара",
                                help_text="Укажите количество товара")
    stronghold = models.CharField(max_length=10, verbose_name='Крепость жидкости/Сопротивление', help_text='Укажите крепость или сопротивление')

    def __str__(self):
        return f"{self.category} - {self.line} - {self.taste}"



class Categories(models.Model):
    category = models.CharField(max_length=100, verbose_name='Название категории', help_text='Введите название категории')
    def __str__(self):
        return self.category


class Line(models.Model):
    line = models.CharField(max_length=100, verbose_name='Название линейки', help_text='Введите название линейки')
    def __str__(self):
        return self.line
