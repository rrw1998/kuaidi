# login/views.py

from django.shortcuts import render, redirect
from . import models
from .form import UserForm, RegisterForm, BusinessForm
import hashlib
from goods.models import Order, Goods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


def index(request):
    print(request.session.get('is_login', None))
    return render(request, 'index.html')


def login(request):
    # 登录
    if request.session.get('is_login', None):
        return redirect("/user/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/user/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    # 注册
    if request.session.get('is_login', None):
        # 登录状态不允许注册。
        return redirect("/user/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return render(request, 'login/pageJump.html', locals())  # 自动跳转
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    # 登出
    if not request.session.get('is_login', None):
        return redirect('/user/')
    request.session.flush()

    return redirect('/user/')


def hash_code(s, salt='mysite_login'):
    # 加密函数
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def become_business(request):
    uid = request.session.get('user_id', None)
    user = models.User.objects.get(id=uid)
    print(user.id)
    if user.is_business == 'b':
        return redirect("/business/")
    if request.method == "POST":
        business_form = BusinessForm(request.POST)
        message = "请检查填写的内容！"
        if business_form.is_valid():  # 获取数据
            company = business_form.cleaned_data['company']
            IDs = business_form.cleaned_data['ID']
            tel = business_form.cleaned_data['tel']
            addr = business_form.cleaned_data['address']

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

            same_name = models.Business.objects.filter(company=company)
            if same_name:  # 用户名唯一
                message = '商家已经存在，请重新选择商家名！'
                return render(request, 'login/become.html', locals())

            new = models.Business.objects.create()
            new.user_id = user.id
            new.company = company
            new.IDs = IDs
            new.tel = tel
            new.province = province
            new.city = city
            new.district = district
            new.address = addr
            new.save()
            user.is_business = 'b'
            user.save()
            return redirect("/business/")  # 自动跳转
    business_form = BusinessForm()
    return render(request, 'login/become.html', locals())


def businessInfo(request):
    uid = request.session.get('user_id', None)
    user = models.User.objects.get(id=uid)
    boss = models.Business.objects.get(user_id=uid)

    return render(request, 'info/business_info.html', locals())


def userInfo(request):
    # 查看用户个人信息
    user = request.session.get('user_id', None)
    userlist = models.User.objects.filter(id=user)
    return render(request, 'info/user_info.html', {'user_list': userlist})


def orderInfo(request):
    user = request.session.get('user_id', None)
    orders = Order.objects.filter(belong_id=user).order_by('-time')
    paginator = Paginator(orders, 5, 2)

    page = request.GET.get('page')
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    return render(request, 'info/order_info.html', locals())


def saleInfo(request):
    uid = request.session.get('user_id', None)
    boss = models.Business.objects.get(user_id=uid)
    good = Goods.objects.filter(shujinn_id=boss.id)
    sale_order = Order.objects.filter().none()
    print(sale_order)
    for g in good:
        print(g)
        order = Order.objects.filter(good=g)
        if order:
            sale_order |= order
    print(sale_order)

    sale_order = sale_order.order_by("-time")
    print(list(sale_order))
    paginator = Paginator(sale_order, 5, 2)
    page = request.GET.get('page')
    try:
        p_order = paginator.page(page)
    except PageNotAnInteger:
        p_order = paginator.page(1)
    except EmptyPage:
        p_order = paginator.page(paginator.num_pages)
    print(page)
    return render(request, 'info/sale.html', locals())


def goodInfo(request):
    good = Goods.objects.filter().all()
    goods = good.order_by("g_id")
    print(goods)
    paginator = Paginator(goods, 6, 2)

    page = request.GET.get('page')
    try:
        show_goods = paginator.page(page)
    except PageNotAnInteger:
        show_goods = paginator.page(1)
    except EmptyPage:
        show_goods = paginator.page(paginator.num_pages)
    return render(request, 'info/good_all_info.html', locals())


def myGoodInfo(request):
    uid = request.session.get('user_id', None)
    boss = models.Business.objects.get(user_id=uid)
    my_goods = Goods.objects.filter(shujinn_id=boss.id).order_by('g_id')
    paginator = Paginator(my_goods, 5, 2)

    page = request.GET.get('page')
    try:
        goods = paginator.page(page)
    except PageNotAnInteger:
        goods = paginator.page(1)
    except EmptyPage:
        goods = paginator.page(paginator.num_pages)
    return render(request, 'info/good_info.html', locals())