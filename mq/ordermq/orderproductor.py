"""
@file: orderproductor.py
@author: rrh
@time: 2020/1/26 9:11 下午
"""
import pika
import json

from HighConcurrence.settings import RABBITHOST, RABBITPORT


class OrderProductor(object):
    def __init__(self, body):
        self.if_connect = False
        self.body = body
        self.conn = None

    def start_publish(self):
        while not self.if_connect:
            self.connect_mq()
        if self.if_connect and self.conn:
            try:
                channel = self.conn.channel()
                exchange = 'order_exchange'
                queue = 'order.111111'
                body = json.dumps(self.body)
                channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
                channel.queue_declare(queue=queue, durable=True)
                channel.queue_bind(exchange=exchange, queue=queue)
                channel.basic_publish(exchange=exchange, body=body, routing_key='order.111111',
                                      properties=pika.BasicProperties(delivery_mode=2))
            except Exception as e:
                print(e)

    def connect_mq(self):
        print('正在重连')
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITHOST, port=RABBITPORT, heartbeat=600,
                                                                      blocked_connection_timeout=300))
        self.if_connect = True
