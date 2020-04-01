"""
@file: startconsume.py
@author: rrh
@time: 2020/3/8 12:48 下午
"""
import threading
import time

from mq.ordermq.orderconsumer import order_consumer, conn
from mq.ordermq.overtimeorderconsumer import overtime_concumer
from mq.ordermq.payconsumer import pay_consumer


def start_consume(goods_id):
    order_consume_thread = threading.Thread(target=order_consumer, args=(goods_id,))
    # t2 = threading.Thread(target=overtime_concumer)
    # t3 = threading.Thread(target=pay_consumer, args=(goods_id,))
    order_consume_thread.start()
    # t2.start()
    # t3.start()

