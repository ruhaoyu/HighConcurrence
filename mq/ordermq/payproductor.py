"""
@file: payproductor.py
@author: rrh
@time: 2020/1/30 9:41 上午
"""
import pika
import json

from HighConcurrence.settings import RABBITHOST, RABBITPORT

conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITHOST, port=RABBITPORT, heartbeat=5))


def save_pay_queue(body):
    channel = conn.channel()
    exchange = 'pay_exchange'
    queue = 'pay_queue'
    routing_key = 'order.' + str(body.get('sale_id')) + '.' + str(body.get('user_id'))
    body = json.dumps(body)
    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue)
    channel.basic_publish(exchange=exchange, body=body, routing_key=routing_key,
                          properties=pika.BasicProperties(delivery_mode=2))
    return
