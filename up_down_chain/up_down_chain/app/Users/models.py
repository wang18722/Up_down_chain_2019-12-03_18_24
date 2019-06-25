from django.contrib.auth.models import AbstractUser
from django.db import models

# UserManager as _UserManager 这样指定才会正确继承，按照django源码命
# 定义用户模型完成后，须去settings，指定AUTH_USER_MODEL = 'users.Users' ('app.类名')，否则django不会辨识
from Enterprise.models import Chain, Provinces

from oauth.models import CustomerInformation


class EnterpriseCertificationInfo(models.Model):
    """企业认证"""
    """认证审核"""
    REVIEWER_LOGO = {
        "STAY": 1,
        "PASS": 2,
        "DEFEAT": 3,

    }
    REVIEWER_STATE = (
        (1, "待审核"),
        (2, "审核通过"),
        (3, "不通过"),
    )
    company_id = models.CharField(max_length=100, primary_key=True, verbose_name="企业id")
    name = models.CharField(max_length=50, verbose_name="企业名字")
    code = models.CharField(max_length=50, verbose_name="信用代码")
    avatar = models.CharField(max_length=200, verbose_name="营业执照")
    contacts = models.CharField(max_length=20, verbose_name="联系人")
    phone = models.CharField(max_length=50, verbose_name="电话号码")
    identity_status = models.SmallIntegerField(choices=REVIEWER_STATE, default=1, verbose_name="审核状态")
    industryid = models.CharField(null=True,max_length=5,verbose_name="行业id")
    create_time = models.DateTimeField(auto_now_add=True,null=True)
    administrator_status = models.CharField(verbose_name='管理员状态', max_length=10, null=True)
    user = models.ForeignKey(CustomerInformation, on_delete=models.CASCADE, verbose_name="关联用户")
    reviewer_time = models.DateField(verbose_name="审核通过时间", null=True)
    reviewer_name = models.CharField(max_length=50, verbose_name="审核人", null=True)
    opinion = models.CharField(max_length=100,verbose_name = "审核意见",null=True)
    province = models.CharField(max_length=20,verbose_name="省份",null=True)
    industry = models.CharField(max_length=100,verbose_name="行业",null=True)
    demand_config = models.CharField(max_length=120, verbose_name="配置需求", default='1')


    class Meta:
        db_table = 'db_EnterpriseCertificationInfo'


class Top_up_Payment(models.Model):
    """支付充值表"""
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总金额")
    userid = models.ForeignKey(EnterpriseCertificationInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = "db_Top_up_Payment"
        verbose_name = "充值表"

        # def __str__(self):
        #     return self.balance


class Record(models.Model):
    """记录表"""
    mobile_count = models.IntegerField(verbose_name="手机号的总数")
    send_count = models.IntegerField(verbose_name="发送短信的总数")
    user = models.ForeignKey(EnterpriseCertificationInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = "db_Record"
        verbose_name = "记录表"


class ManualMessagePost(models.Model):
    """手动营销"""
    customer_id = models.IntegerField(db_column='Customer_id', blank=True, null=True)  # Field name made lowercase.
    industry = models.CharField(db_column='Industry', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    business_scope = models.CharField(db_column='Business_scope', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase.
    filter = models.CharField(db_column='Filter', max_length=255, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=255, blank=True, null=True)
    task_id = models.CharField(db_column='Task_id', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Manual_message_post'


class ManualMessageStatus(models.Model):
    """手动营销"""
    customer_id = models.IntegerField(db_column='Customer_id', blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(db_column='Amount', max_length=255, blank=True,
                              null=True)  # Field name made lowercase.
    task_id = models.CharField(db_column='Task_id', max_length=255, blank=True,
                               null=True)  # Field name made lowercase.
    success = models.CharField(db_column='Success', max_length=255, blank=True,
                               null=True)  # Field name made lowercase.
    unknow = models.CharField(db_column='Unknow', max_length=255, blank=True,
                              null=True)  # Field name made lowercase.
    failed = models.CharField(db_column='Failed', max_length=255, blank=True,
                              null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Manual_message_status'


class Template(models.Model):
    """模板模型"""
    REVIEWER_LOGO = {
        "STAY": 1,
        "PASS": 2,
        "DEFEAT": 3,

    }
    REVIEWER_STATE = (
        (1, "待审核"),
        (2, "审核通过"),
        (3, "不通过"),
    )
    template_name = models.CharField(max_length=50,verbose_name="模板名称")
    sms_type = models.CharField(max_length=50,verbose_name="发送类型")
    data_time = models.DateField(verbose_name="日期",auto_now_add=True)
    user = models.CharField(max_length=50,verbose_name="操作用户")
    content = models.CharField(max_length=500,verbose_name="发送内容")
    reviewer_time = models.DateField(verbose_name="审核通过时间", null=True)
    reviewer_name = models.CharField(max_length=50, verbose_name="审核人", null=True)
    state = models.SmallIntegerField(choices=REVIEWER_STATE, default=1, verbose_name="审核状态")

    class Meta:
        db_table = "db_Template"

class Order(models.Model):
    """短信订单表"""
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    company_id = models.CharField(max_length=100,verbose_name="企业id")
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="订单号")
    total_count = models.IntegerField(default=1, verbose_name="号码总数")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单批总金额")
    sms_type = models.CharField(max_length=50, verbose_name="发送类型")
    username = models.CharField(max_length=50, verbose_name="用户")
    mobile = models.CharField(max_length=2000, verbose_name="手机号")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")

    class Meta:
        db_table = "db_Order"


class ConsumptionRecord(models.Model):
    """短信消费记录表"""
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    enterprise = models.ForeignKey(EnterpriseCertificationInfo, on_delete=models.PROTECT, verbose_name="消费企业")
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name="订单号")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单批总金额")
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="余额")

    class Meta:
        db_table = "db_ConsumptionRecord"

class PayCertificationInfo(models.Model):

    """认证记录表"""
    order_id = models.CharField(max_length=100,verbose_name="订单id",primary_key=True)
    user_id = models.CharField(max_length=15,verbose_name="用户")
    openid = models.CharField(max_length=80,verbose_name="打开id")
    money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    company_name = models.CharField(max_length=100,verbose_name="企业名称")
    mobile = models.CharField(max_length=20,verbose_name="联系人电话")
    name = models.CharField(max_length=20,verbose_name="联系人")

    class Meta:
        db_table = "db_PayCertificationInfo"
