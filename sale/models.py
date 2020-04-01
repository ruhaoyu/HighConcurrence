from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True


class SaleInfo(BaseModel):
    title = models.CharField('商品名称', max_length=500, default='')
    status = models.CharField('状态', max_length=20, default='正常', help_text='正常，删除，下架')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = '商品信息'
        '''按发布日期排序'''
        ordering = ('-create_time',)
        app_label = 'sale'

    def __str__(self):
        return self.title


class Specifications(BaseModel):
    title = models.CharField('规格名称', max_length=1000, default='')
    sale = models.ForeignKey(SaleInfo, on_delete=models.SET_NULL, null=True, related_name='sales', verbose_name='商品')
    num = models.FloatField('库存', default=0)
    price = models.FloatField('价格', default=0)
    status = models.CharField('状态', max_length=20, default='正常', help_text='正常，删除，下架')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = '规格型号'
        '''按发布日期排序'''
        ordering = ('-create_time',)
        app_label = 'sale'

    def __str__(self):
        return self.title

