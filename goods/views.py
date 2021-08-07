import hashlib
import json
from django.shortcuts import redirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from goods.models import Goods, Order
from users.models import User
# Create your views here.
from django.views import View
from .form import OrderForm, GoodForm
from users import models
from traces import models
from traces.models import Trace, Travel
from . import models
from geopy.geocoders import BaiduV3


def createOrder(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        message = "请检查填写的内容！"
        if order_form.is_valid():
            good = order_form.cleaned_data['good']
            user = order_form.cleaned_data['user']
            num = order_form.cleaned_data['gnum']
            addr = order_form.cleaned_data['address']
            # 获得省市区
            jf = open("./static/js/city.js", 'r', encoding='UTF-8')
            jf_str = jf.read()
            jf.close()
            jf_str = jf_str[13:]
            di = json.loads(jf_str)
            pro = request.POST.get("prov")
            pro = int(pro)
            province = di[pro]['name']
            ci = request.POST.get("city")
            ci = int(ci)
            city = di[pro]['city'][ci]['name']
            dis = request.POST.get("district")
            dis = int(dis)
            district = di[pro]['city'][ci]['district'][dis]
            # 信息检查
            user_exist = models.User.objects.filter(id=user)
            good_exist = models.Goods.objects.get(g_id=good)
            if user_exist:
                if not good_exist:
                    message = '商品不存在'
                    return render(request, 'make/create.html', locals())
            else:
                message = '用户不存在'
                return render(request, 'make/create.html', locals())

            # 开始创建
            new_order = models.Order.objects.create()
            id = new_order.id
            print(hashlib.md5(str(id).encode('utf-8')).hexdigest()[8:-8].upper())
            new_order.wl_code = hashlib.md5(str(id).encode('utf-8')).hexdigest()[8:-8].upper()
            new_order.good_id = good
            new_order.gnum = num
            new_order.belong_id = user
            new_order.province = province
            new_order.city = city
            new_order.district = district
            new_order.address = addr
            new_order.save()

            return redirect('/check/')
    order_form = OrderForm()
    return render(request, 'make/create.html', locals())


def checkOrder(request):
    # 订单总价
    uid = request.session.get('user_id', None)
    boss = models.Business.objects.get(user_id=uid)
    good = Goods.objects.filter(shujinn_id=boss.id)
    sale_order = Order.objects.filter().none()
    print(sale_order)
    for g in good:
        print(g)
        orders = Order.objects.filter(good=g)
        if orders:
            sale_order |= orders
    print(sale_order)
    sale_order = sale_order.order_by("-time")
    ord = sale_order[0]
    print(ord.id)
    order = models.Order.objects.get(id=ord.id)
    goods = Goods.objects.get(g_id=order.good_id)
    print(order.gnum, goods.g_price)
    amount = order.gnum * goods.g_price
    order.price = amount
    order.save()
    # 创建轨迹图
    print(order.id)
    print("goods.shujinn_id", goods.shujinn_id)
    boss = models.Business.objects.get(id=goods.shujinn_id)
    new = Trace.objects.create()
    new.order_id = order

    boss_addr = boss.province + boss.city + boss.district + boss.address
    print(boss_addr)
    addr = order.province + order.city + order.district + order.address
    print(addr)
    geolocator = BaiduV3(api_key='FZGNSaym4tjSoZwbSVZEejjfHickKIEB')
    # 商家地址
    location1 = geolocator.geocode(boss_addr)
    print((location1.latitude, location1.longitude))
    new.start_longitude = location1.longitude
    new.start_latitude = location1.latitude

    location2 = geolocator.geocode(addr)
    print((location2.latitude, location2.longitude))
    new.end_longitude = location2.longitude
    new.end_latitude = location2.latitude
    new.save()
    print(new.id)
    # 创建路线
    new_travel = Travel.objects.create()
    new_travel.trace = new
    new_travel.t_time = order.time
    new_travel.now_add = boss.province + boss.city + boss.district
    new_travel.save()
    return render(request, 'make/success.html', locals())


def deleteOrder(request):
    user = request.session.get('user_id', None)
    order = Order.objects.filter(belong_id=user).order_by('-time')
    bid = models.Business.objects.get(user=user)
    ord = order[0]
    trace = Trace.objects.get(order_id_id=ord.id)
    travel = Travel.objects.get(trace_id=trace.id)
    trace.delete()
    travel.delete()
    order[0].delete()
    return redirect('/user/')


def delOrder(request, id):
    order = models.Order.objects.get(id=id)
    print(order.id)
    order.delete()
    return redirect("/order/")


def delGood(request, id):
    good = models.Goods.objects.get(id=id)
    print(good.id)
    good.delete()
    return redirect("/mygood/")


def increase(request):
    if request.method == "POST":
        good_form = GoodForm(request.POST)
        message = "请检查填写的内容！"
        if good_form.is_valid():
            name = good_form.cleaned_data['name']
            price = good_form.cleaned_data['price']

            user = request.session.get('user_id', None)
            boss = models.Business.objects.get(user_id=user)
            print(boss)
            new = models.Goods.objects.create()
            new.g_name = name
            new.g_price = price
            new.shujinn_id = boss.id
            new.save()
            return redirect('/mygood/')
    good_form = GoodForm()
    return render(request, 'make/increase.html', locals())