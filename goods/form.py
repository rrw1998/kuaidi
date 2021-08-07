# _*_coding:utf-8_*_
# 作者    :Rvica
# 日期    :2021/3/8
# 文件    :form.py
# IDE     :PyCharm

from django import forms


class OrderForm(forms.Form):

    # label = "用户名", max_length = 30, widget = forms.TextInput(attrs={'class': 'form-control'})
    good = forms.IntegerField(label="商品", widget=forms.TextInput(attrs={'class': 'form-control'}))
    user = forms.IntegerField(label="用户", widget=forms.TextInput(attrs={'class': 'form-control'}))
    gnum = forms.IntegerField(label="商品数量", widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="详细地址", max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}))


class GoodForm(forms.Form):
    name = forms.CharField(label="商品名称", max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label="商品单价", max_digits=8, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))