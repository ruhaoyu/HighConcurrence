"""
@file: orderconsumer.py
@author: rrh
@time: 2020/1/28 4:48 下午
"""
import json

import pika

from HighConcurrence.settings import RABBITHOST, RABBITPORT
from sale.mysqlop import save_order
conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITHOST, port=RABBITPORT, heartbeat=600,
                                                         blocked_connection_timeout=300))


def save_order_callback(channel, method, properties, body):
    res = save_order(body)
    if res:
        channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        channel.basic_nack(delivery_tag=method.delivery_tag)


def order_consumer(sale_id):
    """订单消费者"""
    print('消费者开始监听')
    channel = conn.channel()
    exchange = 'order.exchange'
    queue = 'order.111111'
    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue, routing_key='order.111111')
    channel.basic_consume(consumer_callback=save_order_callback, queue=queue, no_ack=False)
    channel.start_consuming()
