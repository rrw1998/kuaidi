# _*_coding:utf-8_*_
# 作者    :Rvica
# 日期    :2021/2/22
# 文件    :form.py
# IDE     :PyCharm


from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)


class BusinessForm(forms.Form):
    company = forms.CharField(label="商家名", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ID = forms.CharField(label="身份证号", max_length=18, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tel = forms.CharField(label="电话", max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="详细地址", max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}))

