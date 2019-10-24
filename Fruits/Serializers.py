from rest_framework import serializers

from Fruits.models import FruitUser, Cart, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FruitUser
        fields = ['id', 'f_username', 'f_age', 'f_sex', 'f_phone', 'f_email', 'f_ctime', 'f_icon']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'c_user', 'c_goods', 'c_goods_num', 'is_select']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'o_user', 'o_status', 'o_price', 'o_order_time']
