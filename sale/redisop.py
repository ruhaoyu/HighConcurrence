"""
@file: redisop.py
@author: rrh
@time: 2020/1/26 8:43 下午
redis操作
"""
import redis

from HighConcurrence.settings import REDISHOST, REDISPORT, REDISPW

pool = redis.ConnectionPool(host=REDISHOST, port=REDISPORT, password=REDISPW, db="0", )
redis_conn = redis.Redis(connection_pool=pool)


# 秒杀库存
storage = 100


def plus_counter(goods_id):
    """前一百进入的有秒杀资格，后来的都提示已抢光"""
    count = redis_conn.incr("counter:" + str(goods_id))
    print(count)
    if count > storage:
        return False
    return True


def save_order_redis(data):
    """保存订单到redis提高查询效率"""
    redis_conn.hset("order:" + str(data.get('order_id')), str(data.get('sale_id')), str(data.get('user_id')))


def check_overtime_order_redis(body):
    is_deal = redis_conn.sismember("order:" + str(body.get('sale_id')) + ":" + "deal", str(body.get('order_id')))
    if is_deal:
        return True
    else:
        # 如果没有处理，在redis中添加一条超时记录
        redis_conn.sadd("order:"+str(body.get('sale_id'))+":"+"overtime", str(body.get('order_id')))
        return False


def check_order_status(body):
    # 查询是否超时
    res = redis_conn.sismember("order:"+str(body.get('sale_id'))+":"+"overtime", str(body.get('order_id')))
    if res:
        return -1, '订单已超时'
    else:
        # 查询订单的user_id
        user_id = str(redis_conn.hget("order:" + str(body.get('sale_id')), str(body.get('order_id'))), encoding="utf-8")
        return user_id == body.get('user_id'), ''


def save_pay_redis(body):
    if redis_conn.sismember("order:" + str(body.get('goods_id')) + ":" + "overtime", str(body.get('order_id'))):
        return False
    else:
        redis_conn.sadd("order:" + str(body.get('goods_id')) + ":" + "deal", str(body.get('order_id')))
        return True
