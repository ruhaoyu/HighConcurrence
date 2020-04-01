"""
@file: payconsumer.py
@author: rrh
@time: 2020/3/8 9:43 上午
"""
import pika

from HighConcurrence.settings import RABBITHOST, RABBITPORT
from sale.mysqlop import save_order, save_pay_mysql
from sale.redisop import save_pay_redis

conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITHOST, port=RABBITPORT, heartbeat=4))


def save_pay_callback(channel, method, properties, body):
    res_mysql = save_pay_mysql(body)
    res_redis = save_pay_redis(body)
    if res_mysql and res_redis:
        channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        channel.basic_nack(delivery_tag=method.delivery_tag)


def pay_consumer(sale_id):
    channel = conn.channel()
    exchange = 'pay_exchange'
    queue = 'pay_queue'
    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue, routing_key='order.' + str(sale_id) + '.' + '*')
    channel.basic_consume(consumer_callback=save_pay_callback, queue=queue, no_ack=False)
    channel.start_consuming()
