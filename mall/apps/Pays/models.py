from django.db import models

# Create your models here.
from utils.models import BaseModel


class Wxorder(BaseModel):
    """订单"""
    username = models.CharField(max_length=32, verbose_name='用户名')
    wechat = models.CharField(max_length=32, verbose_name='微信号')
    body = models.CharField(max_length=256, verbose_name="商品描述")
    out_trade_no = models.CharField(max_length=64, unique=True, verbose_name="订单号")
    transaction_id = models.CharField(default="", max_length=64, verbose_name="微信支付订单号")
    total_fee = models.BigIntegerField(verbose_name="订单的资金总额,单位为分")
    product_id = models.CharField(max_length=16, verbose_name="商品ID")
    notify_url = models.CharField(max_length=500, verbose_name="支付完成通知url")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    class Meta:
        verbose_name = "微信订单"
        verbose_name_plural = verbose_name
        # ordering = ('-created_time',)


class Wxpay(BaseModel):
    """
    微信支付
    """
    out_trade_no = models.CharField(null=True, blank=True, max_length=64, verbose_name="订单号")
    pay_no = models.CharField(null=True, blank=True, max_length=64, unique=True, verbose_name="支付唯一订单号")
    code_url = models.CharField(null=True, blank=True, max_length=100, verbose_name="二维码地址")
    nonce_str = models.CharField(null=True, blank=True, max_length=32, verbose_name="随机字符串")

    class Meta:
        verbose_name = "微信支付"
        verbose_name_plural = verbose_name
        # ordering = ('-created_time',)
