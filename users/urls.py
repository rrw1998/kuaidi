# _*_coding:utf-8_*_
# 作者    :Rvica
# 日期    :2021/2/22
# 文件    :urls.py
# IDE     :PyCharm
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^become/', views.become_business),
    url(r'^business/', views.businessInfo),
    url(r'^info/', views.userInfo),
    url(r'^mygood/', views.myGoodInfo),
    url(r'^showgood/', views.goodInfo),
    url(r'^order/', views.orderInfo),
    url(r'^sale/', views.saleInfo),
]