from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response

from FruitServer.models import Goods
from Fruits.Authentication import UserAuthentication
from Fruits.OrderStatus import ORDER_PAY
from Fruits.Serializers import OrderSerializer
from Fruits.models import Order, FruitUser, Cart, OrderGoods, GoodsInfo, OrderAddress, Address, Integral, OrderIntegral
from Fruits.permissions import UserPermission
from Fruits.util import get_all_price


class OrderApiView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = UserAuthentication,
    permission_classes = UserPermission,

    def handle_post(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        if action == 'ordered':
            return self.ordered(request)
        elif action == 'alipay':
            return self.alipay(request)
        elif action == 'checkaddress':
            return self.check_address(request)
        else:
            return self.not_allow_mothed(request)

    def not_allow_mothed(self, request, *agrs, **kwargs):
        data = {
            'msg': '方法不允许',
            'stauts': '401',
        }
        return Response(data)

    def ordered(self, request):
        '''
        需要当前的用户，需要查询购物车里被选中的商品，
        首先找到购物车的产品，遍历这些产品，通过产品找到产品详情信息，然后放到历史订单的商品信息类，在删除购物车里的产品
        将收获地址添加到订单收货地址表里
        '''
        fu = request.user
        price = get_all_price(fu)

        if price == 0:
            data = {
                'msg': '请你先选中需要购买的商品',
                'status': status.HTTP_405_METHOD_NOT_ALLOWED,
            }
            return Response(data)
        order = Order()
        order.o_price = price
        order.o_user = fu
        order.save()
        select_address = Address.objects.filter(is_select=True)
        address = Address.objects.filter(a_user_id=fu.id)

        if address.exists():
            address = address.first()
            if select_address.exists():
                address = select_address.first()

        if not address:
            return Response({'msg': '请你先添加收货地址'})

        # print(address.a_name)
        # return Response({'MSG': 'tiaoshi'})

        carts = Cart.objects.filter(c_user_id=fu.id).filter(is_select=True)
        for cart in carts:
            ordergoods = OrderGoods()
            ordergoods.o_order = order
            ordergoods.o_goods_num = cart.c_goods_num
            ordergoods.save()

            goods = cart.c_goods
            # 将商品信息添加到订单商品信息表中
            goodsinfo = GoodsInfo()
            goodsinfo.g_name = goods.g_name
            goodsinfo.g_price = goods.g_price
            goodsinfo.g_bar_code = goods.g_bar_code
            goodsinfo.g_detail = goods.g_detail
            goodsinfo.g_img = goods.g_img
            goodsinfo.g_market_price = goods.g_market_price
            goodsinfo.g_store_num = cart.c_goods_num

            # 将库存里的数量减少
            goods.g_store_num -= cart.c_goods_num

            goodsinfo.g_type = goods.g_type
            goodsinfo.g_unit = goods.g_unit
            goodsinfo.g_ordergoods = ordergoods
            goods.save()
            # 将收货地址存到订单收获地址中
            orderaddress = OrderAddress()
            orderaddress.order_address_name = address.a_name
            orderaddress.order_address_phone = address.a_phone
            orderaddress.order_address = address.a_address
            orderaddress.ord_id = order.id
            orderaddress.save()

            goodsinfo.save()
            cart.delete()
        data = {
            'msg': 'ok',
            'status': status.HTTP_200_OK,
        }
        return Response(data)

    def alipay(self, request):
        from Fruits.views import pay
        '''
        订单支付，选择需要支付的订单
        :param request:
        :return: Response
        '''
        oid = request.data.get('orderid')

        print(oid)
        order = Order.objects.filter(pk=oid)
        token = request.query_params.get('token')
        if not order.exists():
            return Response({'msg': '请选择你要支付的订单'})
        order = order.first()
        cache.set('oid', order, 60 * 60 * 5)

        url = 'http://127.0.0.1:8000/fruit/order/?token=' + token

        return pay(request, url, order)

    def check_address(self, request):
        aid = request.data.get('aid')
        if not aid:
            data = {
                'msg': '缺少aid参数',
            }
            return Response(data)
        select_address = Address.objects.filter(pk=aid)
        if not select_address.exists():
            data = {
                'msg': '收货地址不存在',
                'status': status.HTTP_400_BAD_REQUEST,
            }
            return Response(data)
        select_address = select_address.first()
        address = Address.objects.all()
        for adre in address:
            adre.is_select = False
            if adre.id == int(aid):
                adre.is_select = True

            adre.save()
        data = {
            'msg': '选择收货地址成功',
            'status': status.HTTP_200_OK,
            '收货人': select_address.a_name,
            '收货地址': select_address.a_address,
            '电话': select_address.a_phone,
        }
        return Response(data)

    def handle_delete(self, request):
        action = request.query_params.get('action')
        if action == 'remove':
            return self.remove(request)
        else:
            return self.not_allow_mothed(request)

    def remove(self, request):
        oid = request.data.get('oid')
        order = Order.objects.filter(pk=oid)
        if not order.exists():
            return Response({'detail': '未找到该订单'})
        # 先找到订单
        order = order.first()
        # 找到订单商品
        ordergoods = OrderGoods.objects.filter(o_order_id=order.id)
        ordergoods = ordergoods.first()
        # 找到订单商品详情
        goodsinfo = GoodsInfo.objects.filter(g_ordergoods_id=ordergoods.id)
        goodsinfo = goodsinfo.first()
        # 找到订单收获地址
        orderaddress = OrderAddress.objects.filter(ord_id=order.id)
        orderaddress = orderaddress.first()
        try:
            goods = Goods.objects.filter(g_bar_code=goodsinfo.g_bar_code).first()
            goods.g_store_num += goodsinfo.g_store_num
            goods.save()
        except Exception as e:
            print('你的商品已经被修改')

        # 由于级联问题，需要由下到上依次删除
        print(ordergoods.id, ordergoods.o_goods_num)
        print(goodsinfo.g_ordergoods_id, goodsinfo.g_name)
        print(orderaddress.id, orderaddress.ord_id)

        orderaddress.delete()
        goodsinfo.delete()
        ordergoods.delete()
        order.delete()

        return Response({'msg': '删除成功'})

    # alipay支付成功后的回调函数
    def handle_get(self, request):

        order = cache.get('oid')
        # order = Order.objects.get(pk=13)

        order.o_status = ORDER_PAY
        order.save()

        ordergoods = OrderGoods.objects.filter(o_order_id=order.id).first()
        Goods.objects.filter(id=ordergoods.id)

        data = {
            'msg': '付款成功',
            'status': status.HTTP_200_OK,
        }
        # 添加到积分记录表
        integral = Integral()
        orderintegral = OrderIntegral()
        orderintegral.ordinteg_id = order.id
        orderintegral.orderscore = order.o_price // 10
        orderintegral.ord_price = order.o_price
        orderintegral.save()

        # 添加积分表
        integral.i_number += orderintegral.orderscore
        integral.i_user_id = order.o_user_id
        integral.save()

        return Response(data)
