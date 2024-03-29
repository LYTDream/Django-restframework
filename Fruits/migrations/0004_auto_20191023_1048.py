# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-10-23 02:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Fruits', '0003_auto_20191022_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_name', models.CharField(max_length=64, verbose_name='收货人')),
                ('a_phone', models.CharField(max_length=32, verbose_name='收货人电话')),
                ('a_address', models.CharField(max_length=264, verbose_name='收货地址')),
                ('a_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Fruits.FruitUser')),
            ],
        ),
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_address_name', models.CharField(max_length=64, verbose_name='收货人')),
                ('order_address_phone', models.CharField(max_length=32, verbose_name='收货人电话')),
                ('order_address', models.CharField(max_length=264, verbose_name='收货地址')),
            ],
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='g_bar_code',
            field=models.CharField(max_length=64, verbose_name='商品编码'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='g_detail',
            field=models.TextField(verbose_name='商品描述'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='g_img',
            field=models.CharField(max_length=128, verbose_name='商品图片'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='g_market_price',
            field=models.FloatField(default=0, verbose_name='超市价格'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='g_name',
            field=models.CharField(max_length=64, verbose_name='商品名称'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='g_price',
            field=models.FloatField(default=0, verbose_name='商品单价'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='g_store_num',
            field=models.IntegerField(default=10, verbose_name='商品数'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='g_unit',
            field=models.CharField(max_length=32, verbose_name='称重类型'),
        ),
        migrations.AlterField(
            model_name='order',
            name='o_order_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='下单时间'),
        ),
        migrations.AlterField(
            model_name='order',
            name='o_price',
            field=models.FloatField(default=0, verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='order',
            name='o_status',
            field=models.IntegerField(default='0', verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='ordergoods',
            name='o_goods_num',
            field=models.IntegerField(default=1, verbose_name='商品数量'),
        ),
        migrations.AddField(
            model_name='orderaddress',
            name='ord',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Fruits.Order'),
        ),
    ]
