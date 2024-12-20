# Generated by Django 5.1.2 on 2024-10-28 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_user_alter_order_order_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(default=1, help_text='Укажите состояние заказа', on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.state', verbose_name='Состояние'),
        ),
    ]
