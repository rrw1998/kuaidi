from django.db import models


# Create your models here.


class User(models.Model):
    # 用户表
    gender = {
        ('male', '男'),
        ('female', '女'),
    }

    ident = (
        ('u', '普通用户'),
        ('b', '商家')
    )

    name = models.CharField(max_length=30, unique=True, verbose_name='姓名')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    sex = models.CharField(max_length=10, choices=gender, default='male', verbose_name='性别')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    is_business = models.CharField(max_length=2, choices=ident, default='u', verbose_name='是否商家')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', null=True)
    company = models.CharField(max_length=50, verbose_name='商家名')
    IDs = models.CharField(max_length=18, verbose_name='身份证号')
    tel = models.CharField(max_length=11, verbose_name='电话')
    province = models.CharField(max_length=16, verbose_name='省')
    city = models.CharField(max_length=16, verbose_name='市')
    district = models.CharField(max_length=16, verbose_name='区')
    address = models.CharField(max_length=100, verbose_name='详细地址')
    b_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')

    def __str__(self):
        return self.company

    class Meta:
        ordering = ['b_time']
        verbose_name = '商家'
        verbose_name_plural = '商家'
