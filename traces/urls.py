# _*_coding:utf-8_*_
# 作者    :Rvica
# 日期    :2021/3/22
# 文件    :urls.py
# IDE     :PyCharm
from django.conf.urls import url
from django.urls import include

from . import views

urlpatterns = [
    # url(r'^/(\d+)/', views.showTrace, name='showTrace'),
    url(r'^/(\d+)/', views.traceInfo, name='traceInfo'),
    url(r'^sport/(\d+)/', views.traceSport, name='showTrace'),
    url(r'^update/(\d+)/', views.updateWay, name='updateWay'),
]