"""
@file: sched_jobs.py
@author: rrh
@time: 2020/3/15 4:14 下午
"""
from apscheduler.schedulers.background import BackgroundScheduler

# from mq.ordermq.orderproductor import conn as order_producter_conn

from mq.ordermq.orderconsumer import conn as order_consumer_conn, order_consumer

sched = BackgroundScheduler()


@sched.scheduled_job('interval', seconds=30)
def conn_mq():
    pass
    # print('重连mq')
    # order_producter_conn.process_data_events()
    # order_consumer_conn.process_data_events()


sched.start()
print('start jobs')
