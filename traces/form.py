# _*_coding:utf-8_*_
# 作者    :Rvica
# 日期    :2021/3/31
# 文件    :form.py
# IDE     :PyCharm

from django import forms


class WayForm(forms.Form):
    longitude = forms.DecimalField(label="经度", max_digits=10, decimal_places=6, widget=forms.TextInput(attrs={'class': 'form-control'}))
    latitude = forms.DecimalField(label="维度", max_digits=10, decimal_places=6, widget=forms.TextInput(attrs={'class': 'form-control'}))
    time = forms.DateTimeField(label="时间", input_formats=['%Y-%m-%d %H:%M'], widget=forms.TextInput(attrs={'class': 'form-control'}))