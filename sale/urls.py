"""
@file: urls.py
@author: rrh
@time: 2020/1/26 2:49 下午
"""
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from sale.views import *

urlpatterns = [
    url(r'^seckill/(?P<pk>\d+)$', csrf_exempt(SaleSeckillView.as_view()), name='sale_seckill'),
    url(r'^seckill/test/$', csrf_exempt(SaleSeckillTestView.as_view()), name='sale_seckill_test'),
]
