# Generated by Django 3.1.6 on 2021-03-27 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210327_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=10, verbose_name='性别'),
        ),
    ]