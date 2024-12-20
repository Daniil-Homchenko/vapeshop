# Generated by Django 5.1.2 on 2024-10-29 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_alter_goods_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='brand',
        ),
        migrations.AddField(
            model_name='goods',
            name='tegs',
            field=models.TextField(blank=True, help_text='Введите теги для поиска товара', null=True, verbose_name='Теги товара'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='description',
            field=models.TextField(blank=True, help_text='Введите описание товара', null=True, verbose_name='Описание товара'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='stronghold',
            field=models.CharField(help_text='Укажите крепость или сопротивление', max_length=10, verbose_name='Крепость жидкости/Сопротивление'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='taste',
            field=models.CharField(blank=True, help_text='Укажите вкус или модель товара', max_length=100, null=True, verbose_name='Вкус/модель товара'),
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
    ]
