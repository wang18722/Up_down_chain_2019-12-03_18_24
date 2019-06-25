
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django.utils import six

class CustomerInformation(AbstractUser):
    """
    用户信息表
    """

    headimgUrl = models.CharField(null=True,max_length=250, verbose_name='微信头像',unique=True)
    sex = models.CharField(null=True, max_length=32, verbose_name='微信性别')
    province = models.CharField(max_length=100, null=True, verbose_name='微信省份')
    city = models.CharField(max_length=32, null=True, verbose_name='微信城市')
    country = models.CharField(max_length=32, null=True, verbose_name=u'微信国家')
    CreateTime = models.DateField(auto_now_add=True, verbose_name="创建时间",null=True,blank=True)

    # 元数据 User下面的子类Meta,
    class Meta:
        db_table = 'tb_Customer_information'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    # USERNAME_FIELD = 'headimgUrl'

class Wxorder(models.Model):
    """订单"""

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


class Wxpay(models.Model):
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




class OAuthWXUser(models.Model):

    user = models.ForeignKey(CustomerInformation,verbose_name="关联的上下链用户")
    openid = models.CharField(verbose_name="微信用户编号",max_length=64,db_index=True)

    class Meta:
        db_table = "tb_oauth_wx"
        verbose_name = "微信用户数据"
        verbose_name_plural = verbose_name