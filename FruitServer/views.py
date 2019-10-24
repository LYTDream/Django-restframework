from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response

from FruitServer.Serizlizer import TypeOneSerializer, GoodsSerializer
from FruitServer.models import GoodsTypeOne, Goods


class GoodsTypeAPIView(viewsets.ModelViewSet):
    queryset = GoodsTypeOne.objects.all()
    serializer_class = TypeOneSerializer

    def get_goodstypes(self, request, *args, **kwargs):
        data = {
            "msg": "ok",
            "status": status.HTTP_200_OK,
            "types": self.list(request).data,
        }

        return Response(data)


class GoodsAPIView(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # 筛选  一级标识   二级标识（可选）  三级排序（可选）
        typeone = self.request.query_params.get("typeone")
        typetwo = self.request.query_params.get("typetwo")
        sortrule = self.request.query_params.get("sortrule")

        if not typeone:
            raise exceptions.APIException(detail="请提供正确的参数")

        queryset = queryset.filter(g_type__g_one_id=typeone)

        if typetwo:
            queryset = queryset.filter(g_type_id=typetwo)

        if sortrule == 1:
            queryset = queryset.order_by("g_price")
            # 价格升序
        elif sortrule == 2:
            queryset = queryset.order_by("-g_price")
            # 价格降序

        return queryset
