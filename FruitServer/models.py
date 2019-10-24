from django.db import models


class GoodsTypeOne(models.Model):
    g_name = models.CharField(max_length=32, unique=True, verbose_name='商品种类')

    def __str__(self):
        return self.g_name

    class Meta:
        verbose_name_plural = '商品一级表'


class GoodsTypeTwo(models.Model):
    g_name = models.CharField(max_length=32, verbose_name='商品类型')
    g_one = models.ForeignKey(GoodsTypeOne, related_name="goodstypetwos", verbose_name='种类编号')

    class Meta:
        verbose_name_plural = '商品二级表'

    def __str__(self):
        return self.g_name


class Goods(models.Model):
    g_name = models.CharField(max_length=64, verbose_name='商品名称')
    g_price = models.FloatField(default=0, verbose_name='商品单价')
    g_market_price = models.FloatField(default=0, verbose_name='超市价格')
    g_unit = models.CharField(max_length=32, verbose_name='称重类型')
    g_detail = models.TextField(verbose_name='商品描述')
    g_img = models.CharField(max_length=128, verbose_name='商品图片')
    g_bar_code = models.CharField(max_length=64, verbose_name='商品编码')
    g_store_num = models.IntegerField(default=10, verbose_name='商品数')
    g_type = models.ForeignKey(GoodsTypeTwo, verbose_name='商品类型')

    class Meta:
        verbose_name_plural = '商品信息表'

    def __str__(self):
        return self.g_name
