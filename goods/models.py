from django.db import models
from users.models import *
# Create your models here.
from django.utils import timezone
import random


class Goods(models.Model):
    # 商品表
    g_id = models.BigAutoField(primary_key=True, verbose_name='商品号')
    g_name = models.CharField(max_length=100, verbose_name='商品名', null=True)  # 商品名
    g_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='商品价格', null=True)  # 商品价格
    shujinn = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name='商家', null=True)

    def __str__(self):
        return self.g_name

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'


class Order(models.Model):
    # 订单表
    ostatus = {
        ('1', '派送中'),
        ('2', '已送达')
    }

    wl_code = models.CharField(max_length=16, unique=True, verbose_name='订单号', null=True)
    status = models.CharField(max_length=16, choices=ostatus, default='1', verbose_name='订单状态')
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品', null=True)  # 商品
    gnum = models.IntegerField(verbose_name='商品数量', default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='价格', null=True)
    belong = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', null=True)  # 用户ID
    time = models.DateTimeField(default=timezone.now, verbose_name='下单时间')  # 商品下单时间
    province = models.CharField(max_length=16, verbose_name='省')
    city = models.CharField(max_length=16, verbose_name='市')
    district = models.CharField(max_length=16, verbose_name='区')
    address = models.CharField(max_length=100, verbose_name='详细地址')  # 收件地址

    def __str__(self):
        return self.wl_code

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'



