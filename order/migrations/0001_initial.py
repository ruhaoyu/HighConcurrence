# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2020-03-13 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('order_no', models.CharField(default='', max_length=500, verbose_name='订单编号')),
                ('user_id', models.IntegerField(null=True, verbose_name='下单用户')),
                ('status', models.CharField(default='正常', help_text='正常,删除,超时', max_length=20, verbose_name='状态')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('order_id', models.IntegerField(null=True, verbose_name='订单')),
                ('pay_time', models.DateTimeField(auto_now_add=True, verbose_name='支付时间')),
                ('user_id', models.IntegerField(null=True, verbose_name='支付用户')),
                ('pay_way', models.CharField(default='alipay', max_length=20, verbose_name='支付方式')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Snap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('sale_id', models.IntegerField(null=True, verbose_name='商品id')),
                ('order_id', models.IntegerField(null=True, verbose_name='订单id')),
                ('price', models.FloatField(default=0, verbose_name='交易价格')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]