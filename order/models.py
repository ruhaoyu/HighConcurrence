from django.db import models


# Create your models here.


class OrderBaseModel(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True


class Order(OrderBaseModel):
    order_no = models.CharField('订单编号', max_length=500, default='')
    user_id = models.IntegerField('下单用户', null=True)
    status = models.CharField('状态', max_length=20, default="正常", help_text='正常,删除,超时')

    class Meta:
        app_label = 'order'

class Snap(OrderBaseModel):
    sale_id = models.IntegerField('商品id', null=True)
    order_id = models.IntegerField('订单id', null=True)
    price = models.FloatField('交易价格', default=0)

    class Meta:
        app_label = 'order'


class Pay(OrderBaseModel):
    order_id = models.IntegerField('订单', null=True)
    pay_time = models.DateTimeField('支付时间', auto_now_add=True)
    user_id = models.IntegerField('支付用户', null=True)
    pay_way = models.CharField('支付方式', max_length=20, default='alipay')

    class Meta:
        app_label = 'order'
