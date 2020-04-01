"""
@file: overtimeorderproductor.py
@author: rrh
@time: 2020/1/28 3:08 下午
"""

import pika
import json

from HighConcurrence.settings import RABBITHOST, RABBITPORT
from mq.ordermq import TIMEOUT

conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITHOST, port=RABBITPORT, heartbeat=3))


def save_order_overtime_queue(body):
    channel = conn.channel()

    # ----------------接收超时交换机----------------
    exchange = 'order_overtime_exchange'
    # 接收超时队列
    queue = 'order_overtime_queue'
    channel.exchange_declare(exchange=exchange, durable=True, exchange_type='fanout')
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue)
    # ----------------接收超时交换机结束----------------

    # ----------------延时交换机----------------
    exchange_delay = 'order_overtime_exchange_delay'
    queue_delay = 'order_overtime_queue_delay'
    channel.exchange_declare(exchange=exchange_delay, durable=True, exchange_type='fanout')
    args = {
        'x-message-ttl': 1000 * 60 * TIMEOUT,  # 延迟时间 （毫秒） TIMEOUT分钟
        'x-dead-letter-exchange': exchange,  # 延迟结束后指向交换机
        'x-dead-letter-routing-key': queue,  # 延迟结束后指向队列
    }

    channel.queue_declare(queue=queue_delay, durable=True, arguments=args)
    channel.queue_bind(exchange=exchange_delay, queue=queue_delay)
    # ----------------延时交换机结束----------------

    body = json.dumps(body)

    channel.basic_publish(exchange=exchange_delay, body=body, routing_key='',
                          properties=pika.BasicProperties(delivery_mode=2))
