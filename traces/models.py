from django.db import models
from goods.models import *


# Create your models here.


class Trace(models.Model):
    # 轨迹表
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单', null=True)
    start_longitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='起点经度', null=True)
    end_longitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='终点经度', null=True)
    start_latitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='起点纬度', null=True)
    end_latitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='终点纬度', null=True)

    class Meta:
        verbose_name = '轨迹'
        verbose_name_plural = '轨迹'


class Way(models.Model):
    # 路程表
    trace_id = models.ForeignKey(Trace, on_delete=models.CASCADE, verbose_name='轨迹', null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='经度', null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='纬度', null=True)
    w_time = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name='时间', null=True)

    class Meta:
        verbose_name = '路程'
        verbose_name_plural = '路程'


class Travel(models.Model):
    trace = models.ForeignKey(Trace, on_delete=models.CASCADE, verbose_name='轨迹', null=True)
    t_time = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name='时间', null=True)
    now_add = models.CharField(max_length=258, verbose_name='位置', null=True)

    class Meta:
        verbose_name = '位置变换'
        verbose_name_plural = '位置变换'
