from django.contrib.auth.hashers import check_password
from django.db import models

# Create your models here.
from FruitServer.models import Goods, GoodsTypeTwo
from Fruits.OrderStatus import ORDER_ORDERED


class FruitUser(models.Model):
    f_username = models.CharField(max_length=32, unique=True)
    f_password = models.CharField(max_length=128, null=True)
    f_age = models.IntegerField(default=0)
    f_sex = models.BooleanField(default=False)
    f_phone = models.CharField(max_length=32, unique=True)
    f_email = models.CharField(max_length=32, unique=True)
    f_icon = models.CharField(max_length=64, null=True)
    f_ctime = models.DateTimeField(auto_now_add=True, null=True)
    f_activated = models.BooleanField(default=False)
    f_disabled = models.BooleanField(default=False)
    f_delete = models.BooleanField(default=False)

    def verify_password(self, password):
        return check_password(password, self.f_password)

    def __str__(self):
        return self.f_username


class Cart(models.Model):
    c_user = models.ForeignKey(FruitUser)
    c_goods = models.ForeignKey(Goods)

    c_goods_num = models.IntegerField(default=1, verbose_name='数量')
    is_select = models.BooleanField(default=True, verbose_name='是否选中')


class Order(models.Model):
    o_user = models.ForeignKey(FruitUser)
    o_status = models.IntegerField(default=ORDER_ORDERED, verbose_name='状态')
    o_price = models.FloatField(default=0, verbose_name='价格')
    o_order_time = models.DateTimeField(auto_now_add=True, verbose_name='下单时间')

    class Meta:
        verbose_name_plural = '订单表'

    def order_user_name(self):
        return self.o_user.f_username

    order_user_name.short_description = '下单用户名'


class OrderGoods(models.Model):
    o_order = models.ForeignKey(Order)
    o_goods_num = models.IntegerField(default=1, verbose_name='商品数量')


class GoodsInfo(models.Model):
    g_ordergoods = models.OneToOneField(OrderGoods)

    g_name = models.CharField(max_length=64, verbose_name='商品名称')
    g_price = models.FloatField(default=0, verbose_name='商品单价')
    g_market_price = models.FloatField(default=0, verbose_name='超市价格')
    g_unit = models.CharField(max_length=32, verbose_name='称重类型')
    g_detail = models.TextField(verbose_name='商品描述')
    g_img = models.CharField(max_length=128, verbose_name='商品图片')
    g_bar_code = models.CharField(max_length=64, verbose_name='商品编码')
    g_store_num = models.IntegerField(default=10, verbose_name='商品数')
    g_type = models.ForeignKey(GoodsTypeTwo)


class Address(models.Model):
    a_name = models.CharField(max_length=64, verbose_name='收货人')
    a_phone = models.CharField(max_length=32, verbose_name='收货人电话')
    a_address = models.CharField(max_length=264, verbose_name='收货地址')
    is_select = models.BooleanField(default=True)
    a_user = models.ForeignKey(FruitUser)


class OrderAddress(models.Model):
    order_address_name = models.CharField(max_length=64, verbose_name='收货人')
    order_address_phone = models.CharField(max_length=32, verbose_name='收货人电话')
    order_address = models.CharField(max_length=264, verbose_name='收货地址')
    ord = models.OneToOneField(Order)

    class Meta:
        verbose_name_plural = '订单收货地址表'

    def ord_user(self):
        return self.ord.o_user.f_username

    ord_user.short_description = '下单人'


class Integral(models.Model):
    i_number = models.IntegerField(default=0, verbose_name='积分')
    i_user = models.ForeignKey(FruitUser)


class OrderIntegral(models.Model):
    ordinteg = models.OneToOneField(Order)
    orderscore = models.IntegerField(verbose_name='积分分值')
    ord_price = models.FloatField(default=0, verbose_name='订单价格')
    order_integ_time = models.DateTimeField(auto_now_add=True, verbose_name='积分创建时间')

    class Meta:
        verbose_name_plural = '订单积分表'
