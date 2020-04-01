"""
@file: overtimeorderconsumer.py
@author: rrh
@time: 2020/1/29 10:17 下午
"""
import json
import pika

from HighConcurrence.settings import RABBITHOST, RABBITPORT
from sale.mysqlop import update_order_status
from sale.redisop import check_overtime_order_redis

conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITHOST, port=RABBITPORT, heartbeat=2))


def overtime_order_call_back(channle, method, properties, body):
    body = json.loads(body)
    res = check_overtime_order_redis(body)
    if not res:
        # 如果没有处理，去修改订单的状态
        update_order_status(body, '超时')
    channle.basic_ack(delivery_tag=method.delivery_tag)


def overtime_concumer():
    channel = conn.channel()
    exchange = 'order_overtime_exchange'
    queue = 'order_overtime_queue'
    channel.exchange_declare(exchange=exchange, durable=True, exchange_type='fanout')
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_consume(consumer_callback=overtime_order_call_back, queue=queue, no_ack=False)
    channel.start_consuming()
