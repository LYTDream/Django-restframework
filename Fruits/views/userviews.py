import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Fruits.Authentication import UserAuthentication
from Fruits.Serializers import UserSerializer
from Fruits.models import FruitUser
from Fruits.permissions import UserPermission
from Fruits.task import send_activate_email_async
from Fruits.util import send_email


class UsersApiView(viewsets.ModelViewSet):
    queryset = FruitUser.objects.all()
    serializer_class = UserSerializer

    def handle_post(self, request, *agrs, **kwargs):
        print('_' * 50)
        action = request.query_params.get('action')
        if action == 'login':
            return self.do_login(request, *agrs, **kwargs)
        elif action == 'register':
            return self.do_register(request, *agrs, **kwargs)
        elif action == 'check_name':
            return self.check_name(request, *agrs, **kwargs)
        elif action == 'check_phone':
            return self.check_phone(request, *agrs, **kwargs)
        elif action == 'check_email':
            return self.check_email(request, *agrs, **kwargs)
        else:
            return self.not_allow_mothed(request)

    def handle_get(self, request, *agrs, **kwargs):
        action = request.query_params.get('action')
        if action == 'activation':
            return self.activation(request, *agrs, **kwargs)
        else:
            return self.not_allow_mothed(request)

    def do_login(self, request, *agrs, **kwargs):
        f_name = request.data.get('f_name')
        f_password = request.data.get('f_password')
        if f_name and f_password:
            fu = FruitUser.objects.filter(f_username=f_name)
            if fu:
                fu = fu.first()
                if fu.verify_password(f_password):
                    token = uuid.uuid4().hex
                    cache.set(token, fu, 60 * 60 * 60)
                    print(cache.get(token))

                    data = {
                        'msg': '登陆成功',
                        'token': token,
                        'username': fu.f_username,
                    }

                    return Response(data)
                return Response({
                    'msg': '用户名或密码错误！',
                })
            return Response({
                'msg': '请你先注册！',
            })
        else:
            return Response({
                'msg': '用户米或密码不能为空！'
            })

    def do_register(self, request, *agrs, **kwargs):

        self.create(request, *agrs, **kwargs)

        data = {
            'msg': '注册成功',
            'status': status.HTTP_200_OK,
        }
        task_id = send_activate_email_async.delay(request.data.get('f_username'), request.data.get('f_email'))
        print(task_id)
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(f_password=make_password(self.request.data.get('f_password')))

    def check_name(self, request, *agrs, **kwargs):
        print('check_name')
        f_name = request.data.get('f_name')
        fu = FruitUser.objects.filter(f_username=f_name)
        data = {
            'msg': '',
            'stauts': 200,
        }
        if fu:
            data.update({'msg': '用户名已存在'})
            return Response(data)
        data.update({'msg': '用户名可以使用'})
        return Response(data)

    def check_phone(self, request, *agrs, **kwargs):
        print('check_phone')
        f_phone = request.data.get('f_phone')
        fu = FruitUser.objects.filter(f_phone=f_phone)
        data = {
            'msg': '',
            'stauts': 200,
        }
        if fu:
            data.update({'msg': '手机号已存在'})
            return Response(data)
        data.update({'msg': '手机号可以使用'})
        return Response(data)

    def check_email(self, request, *agrs, **kwargs):
        print('check_email')
        f_email = request.data.get('f_email')
        fu = FruitUser.objects.filter(f_email=f_email)
        data = {
            'msg': '',
            'stauts': 200,
        }
        if fu:
            data.update({'msg': '邮箱已存在'})
            return Response(data)
        data.update({'msg': '邮箱可以使用'})
        return Response(data)

    def not_allow_mothed(self, request, *agrs, **kwargs):
        data = {
            'msg': '方法不允许',
            'stauts': '401',
        }
        return Response(data)

    def activation(self, request, *agrs, **kwargs):
        token = request.query_params.get('token')
        uname = cache.get(token)

        fu = FruitUser.objects.filter(f_username=uname)
        if not fu:
            return Response({'msg': '没有当前用户'})
        fu = fu.first()
        if fu.f_activated:
            cache.delete(token)
            return Response({'msg': '你已经激活账户，请勿重新激活！'})
        fu.f_activated = True
        fu.save()
        data = {
            'msg': '激活成功',
            'status': status.HTTP_200_OK,
        }
        return Response(data)


class UserApiView(RetrieveUpdateDestroyAPIView):
    queryset = FruitUser.objects.all()
    serializer_class = UserSerializer

    authentication_classes = UserAuthentication,
    permission_classes = UserPermission,
