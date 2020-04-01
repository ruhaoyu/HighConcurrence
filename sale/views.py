import datetime
import json
import uuid

import gevent
import requests
from django.http import JsonResponse, HttpResponse

# Create your views here.
from django.views import View

from mq.ordermq.payproductor import save_pay_queue
from sale.redisop import plus_counter, save_order_redis, check_order_status, save_pay_redis
# from mq.ordermq.orderproductor import save_order_queue
from mq.ordermq.orderproductor import OrderProductor
from mq.ordermq.overtimeorderproductor import save_order_overtime_queue


class SaleSeckillView(View):

    def get(self, request, pk):
        return HttpResponse('测试')

    def post(self, request, pk):
        # user = request.user
        if plus_counter(pk):
            order = {
                'order_id': str(1),
                'user_id': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                # 'user_id': user.id,
                'sale_id': pk
            }
            # 订单信息存在redis提高查询效率
            save_order_redis(order)
            # 订单信息写入队列
            OrderProductor(order).start_publish()
            # 订单信息写入超时队列
            # save_order_overtime_queue(order)

            code = 1
            msg = '恭喜抢购成功，请在十五分钟内付款，否则会取消订单！'

            # try:
            #     # 订单信息存在redis提高查询效率
            #     save_order_redis(order)
            #     # 订单信息写入队列
            #     save_order_queue(order)
            #     # 订单信息写入超时队列
            #     save_order_overtime_queue(order)
            #
            #     code = 1
            #     msg = '恭喜抢购成功，请在十五分钟内付款，否则会取消订单！'
            # except Exception as e:
            #     print(e)
            #     code = 0
            #     msg = '抢购出错，请重试！'
        else:
            code = 0
            msg = '已抢光'
        print('log', msg)
        return JsonResponse({'code': code, 'msg': msg})


class Pay(View):
    def post(self, request, order_id, user_id, sale_id):
        body = {
            'order_id': order_id,
            'user_id': user_id,
            'sale_id': sale_id
        }
        order_status, msg = check_order_status(body)
        if order_status:
            if order_status == -1:
                return JsonResponse({'code': 0, 'msg': msg})
            else:
                # 支付省
                # pay = Alipay()
                # 写入队列和redis
                save_pay_queue(body)
                save_pay_redis(body)
                return JsonResponse({'code': 1, 'msg': '支付成功'})
        return JsonResponse({'code': 0, 'msg': '参数错误'})


def testseckill(i):
    print('第{}次测试'.format(str(i)))
    r = requests.post('http://192.168.1.110:8000/sale/seckill/1')


class SaleSeckillTestView(View):
    def get(self, request):
        run_gevent_list = []
        for i in range(1000001):
            run_gevent_list.append(gevent.spawn(testseckill(i)))
        gevent.joinall(run_gevent_list)
        return HttpResponse('ok')
