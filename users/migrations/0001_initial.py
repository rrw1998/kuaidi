# Generated by Django 3.1.6 on 2021-03-27 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='姓名')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=10, verbose_name='性别')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['c_time'],
            },
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50, verbose_name='商家名')),
                ('IDs', models.CharField(max_length=18, verbose_name='身份证号')),
                ('tel', models.CharField(max_length=11, verbose_name='电话')),
                ('province', models.CharField(max_length=16, verbose_name='省')),
                ('city', models.CharField(max_length=16, verbose_name='市')),
                ('district', models.CharField(max_length=16, verbose_name='区')),
                ('address', models.CharField(max_length=100, verbose_name='详细地址')),
                ('b_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '商家',
                'verbose_name_plural': '商家',
                'ordering': ['b_time'],
            },
        ),
    ]