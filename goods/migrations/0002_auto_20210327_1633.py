# Generated by Django 3.1.6 on 2021-03-27 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='wl_ship',
            field=models.CharField(choices=[('HHTT', '天天快递'), ('HTKY', '百世快递'), ('YTO', '圆通快递'), ('STO', '申通快递')], max_length=10, verbose_name='快递公司'),
        ),
    ]
