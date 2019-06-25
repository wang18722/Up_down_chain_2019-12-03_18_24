from django.db import models
from oauth.models import CustomerInformation


class OrderInfo(models.Model):
    """
    支付订单信息
    """

    order_id = models.CharField(max_length=64, verbose_name="订单号")
    mch_id = models.CharField(max_length=32,verbose_name="商户号")
    result_code = models.CharField(max_length=16,verbose_name="业务结果")
    openid = models.CharField(max_length=128,verbose_name="用户标识")
    trade_type = models.CharField(max_length=32,verbose_name="交易类型")
    is_subscribe = models.CharField(max_length=1,verbose_name="是否关注公众账号",default="N")
    pay_result = models.SmallIntegerField(verbose_name="支付结果")
    transaction_id = models.CharField(max_length=32,verbose_name="平台订单号")
    out_transaction_id = models.CharField(max_length=32,primary_key=True, verbose_name="第三方订单号")
    out_trade_no = models.CharField(max_length=32,verbose_name="商户订单号")
    total_fee = models.SmallIntegerField(verbose_name="总金额")
    bank_type = models.CharField(max_length=16,null=True,blank=True,verbose_name="付款银行")
    time_end = models.CharField(max_length=14,verbose_name="支付完成时间")

    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


    class Meta:
        db_table = "payment_record"
        verbose_name = "支付记录表"
