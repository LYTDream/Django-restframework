# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-10-23 11:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Fruits', '0005_address_is_select'),
    ]

    operations = [
        migrations.CreateModel(
            name='Integral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i_number', models.IntegerField(default=0, verbose_name='积分')),
                ('i_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Fruits.FruitUser')),
            ],
        ),
        migrations.CreateModel(
            name='OrderIntegral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderscore', models.IntegerField(verbose_name='积分分值')),
                ('ord_price', models.FloatField(default=0, verbose_name='订单价格')),
                ('order_integ_time', models.DateTimeField(auto_now_add=True, verbose_name='积分创建时间')),
                ('ordinteg', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Fruits.Order')),
            ],
        ),
    ]
