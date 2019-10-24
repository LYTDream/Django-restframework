from django.contrib import admin

# Register your models here.
from FruitServer.models import Goods, GoodsTypeOne, GoodsTypeTwo
from Fruits.models import Order, OrderAddress, OrderIntegral, OrderGoods


class FruitAdmin(admin.ModelAdmin):
    fields = (
        'g_name', 'g_price', 'g_market_price', 'g_unit', 'g_detail', 'g_img', 'g_bar_code', 'g_store_num', 'g_type')
    list_display = (
        'id', 'g_name', 'g_price', 'g_market_price', 'g_unit', 'g_detail', 'g_img', 'g_bar_code', 'g_store_num',
        'g_type_id')


class TypeOneAdmin(admin.ModelAdmin):
    list_display = ('g_name',)
    fields = ('g_name',)


class TypeTwoAdmin(admin.ModelAdmin):
    def get_one_name(self):
        return self

    list_display = ('g_name', 'g_one_id')
    fields = ('g_name', 'g_one')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_user_name', 'o_status', 'o_price', 'o_order_time')


class OrderAddressAdmin(admin.ModelAdmin):
    list_display = ('id', "order_address_name", "order_address_phone", "order_address", "ord_user")


class InterAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderscore', 'ord_price', 'order_integ_time')


class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'o_order_id', 'o_goods_num')


admin.site.register(Goods, FruitAdmin)
admin.site.register(GoodsTypeOne, TypeOneAdmin)
admin.site.register(GoodsTypeTwo, TypeTwoAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderGoods, OrderGoodsAdmin)
admin.site.register(OrderAddress, OrderAddressAdmin)
admin.site.register(OrderIntegral, InterAdmin)
