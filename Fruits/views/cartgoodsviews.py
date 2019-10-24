from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from FruitServer.models import Goods
from Fruits.Authentication import UserAuthentication
from Fruits.Serializers import UserSerializer, CartSerializer
from Fruits.models import FruitUser, Cart
from Fruits.permissions import UserPermission, CartUserPermission


class CartsApiView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = UserAuthentication,
    permission_classes = UserPermission,

    def handle_post(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        if action == 'addcart':
            return self.add_cart(request)
        elif action == 'selected':
            return self.selected(request)
        else:
            return self.not_allow_mothed(request)

    def handle_delete(self, request, *args, **kwargs):
        carts = Cart.objects.filter(is_select=True)
        if not carts.exists():
            data = {
                'msg': '请你先选中要删除的商品',
            }
            return Response(data)
        for cart in carts:
            cart.delete()

        data = {
            'msg': '删除成功',
            'status': status.HTTP_200_OK,
        }
        return Response(data)

    def not_allow_mothed(self, request, *agrs, **kwargs):
        data = {
            'msg': '方法不允许',
            'stauts': '401',
        }
        return Response(data)

    def add_cart(self, request):
        fu = request.user
        if not fu:
            data = {
                'msg': '你的身份已过期,请你重新登录',
            }
            return Response(data)
        gid = request.data.get('good_id')
        gnum = request.data.get('good_num')
        print(gid, gnum)
        cart = Cart.objects.filter(c_user=request.user).filter(c_goods_id=gid)
        if cart.exists():
            cart = cart.first()
            cart.c_goods_num += int(gnum)

        else:
            cart = Cart()
            cart.c_user = request.user
            cart.c_goods_id = gid
            cart.c_goods_num = gnum or 1

        cart.save()

        data = {
            'msg': 'ok',
            'status': status.HTTP_200_OK,
        }
        return Response(data)

    def selected(self, request):
        carts = Cart.objects.filter(is_select=False)
        ''' 
            如果全都是选中的，变成全都未选中
            如果有一个是未选中的，变成全都选中
        '''
        if not carts.exists():
            carts = Cart.objects.all()
            for cart in carts:
                cart.is_select = False
                cart.save()
            data = {
                'msg': '你的购物车已经全部未选中',
                'status': status.HTTP_200_OK,
            }
            return Response(data)
        for cart in carts:
            cart.is_select = True
            cart.save()
        data = {
            'msg': '你的购物车已经全部选中，请及时下单',
            'status': status.HTTP_200_OK,
        }
        return Response(data)


class CartApiView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = UserAuthentication,
    permission_classes = CartUserPermission,

    def handle_post(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        pk = kwargs.get('pk')

        if action == 'addnum':
            return self.add_num(request, pk)
        elif action == 'delnum':
            return self.del_num(request, pk)
        elif action == 'selected':
            return self.selected(request, pk)
        else:
            return self.not_allow_mothed(request)

    def not_allow_mothed(self, request, *agrs, **kwargs):
        data = {
            'msg': '方法不允许',
            'stauts': '401',
        }
        return Response(data)

    def add_num(self, request, pk):
        print(request.user)
        cart = Cart.objects.filter(pk=pk).filter(c_user_id=request.user.id)
        if not cart.exists():
            data = {
                'msg': '商品id错误',
                'status': status.HTTP_400_BAD_REQUEST,
            }
            return Response(data)
        cart = cart.first()

        cart.c_goods_num += 1
        cart.save()
        data = {
            'msg': '数量加一',
            'status': status.HTTP_200_OK,
        }
        return Response(data)

    def del_num(self, request, pk):
        cart = Cart.objects.filter(pk=pk).filter(c_user_id=request.user.id)

        if not cart.exists():
            data = {
                'msg': '商品id错误',
                'status': status.HTTP_400_BAD_REQUEST,
            }
            return Response(data)
        cart = cart.first()

        cart.c_goods_num -= 1
        cart.save()

        data = {
            'msg': '数量减一',
            'status': status.HTTP_200_OK,
        }
        return Response(data)

    def selected(self, request, pk):
        cart = Cart.objects.filter(pk=pk).filter(c_user_id=request.user.id)

        if not cart.exists():
            data = {
                'msg': '商品id错误',
                'status': status.HTTP_400_BAD_REQUEST,
            }
            return Response(data)
        cart = cart.first()
        data = {
            'msg': '商品已选中',
            'status': status.HTTP_200_OK,
        }
        if cart.is_select:
            cart.is_select = False
            data.update({'msg': '商品已取消'})
        cart.is_select = True
        cart.save()

        return Response(data)
