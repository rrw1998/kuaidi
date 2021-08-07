# _*_coding:utf-8_*_
# 作者    :Rvica
# 日期    :2021/3/8
# 文件    :urls.py
# IDE     :PyCharm

from django.conf.urls import url
from django.urls import include

from . import views

urlpatterns = [
    url(r'^create/', views.createOrder),
    url(r'^check/', views.checkOrder, name="check"),
    url(r'^delete/', views.deleteOrder),
    url(r'^delOrder/(\d+)/', views.delOrder, name="delOrder"),
    url(r'^delGood/(\d+)/', views.delGood, name="delGood"),
    url(r'^increase/', views.increase),
]