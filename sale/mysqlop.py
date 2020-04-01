"""
@file: mysqlop.py
@author: rrh
@time: 2020/1/28 8:04 下午
mysql操作
"""

# 消费队列回调函数，保存订单
import json

from django.db import transaction

from order.models import Snap, Order
from sale.models import Specifications


def save_order(body):
    print('消费者保存订单到数据库')
    body = json.loads(body)
    order_id = body.get('order_id')
    sale_id = body.get('sale_id')
    user_id = body.get('user_id')
    sale = Specifications.objects.filter(id=sale_id).first()
    price = sale and sale.price or 0
    with transaction.atomic():
        try:
            snap = Snap.objects.create(order_id=order_id, sale_id=sale_id, price=price)
            order = Order.objects.create(order_no=order_id)
        except Exception as e:
            print(e)
            return False
        return True


def update_order_status(body, status):
    Order.objects.filter(order_no=str(body.get('order_id'))).update(status=status)


def save_pay_mysql(body):
    if not body:
        return False
    sale = Specifications.objects.filter(id=body.get('sale_id')).first()
    price = sale.price or 0
    Pay.objects.create(order_id=body.get('order_id'), sale_id=body.get('sale_id'), price=price)
    return True
