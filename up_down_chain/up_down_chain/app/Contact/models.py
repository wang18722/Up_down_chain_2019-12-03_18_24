from django.db import models

# Create your models here.



# class AiMarketing(models.Model):
#     """AI自动营销模型类"""
#     mobile = models.CharField(max_length=1000,verbose_name="手机号")
#     marketing = models.CharField(max_length=30,verbose_name="营销名称")
#     mobile_count = models.IntegerField(verbose_name="号码数量")
#     push_industries = models.CharField(max_length=100,verbose_name="推送行业")
#     the_main = models.CharField(max_length=100,verbose_name="主营")
#     push_region = models.CharField(max_length=100,verbose_name="推送地区")
#     send_time = models.TimeField(auto_now=True,verbose_name="发送时间")
#     out_state = models.BooleanField(verbose_name="排除状态")
#     send_message_count = models.IntegerField(verbose_name="发送短信数量")
#     successful = models.IntegerField(verbose_name="成功数")
#     unknown = models.IntegerField(verbose_name="未知数")
#     send_date = models.DateField(auto_now=True,verbose_name="发送日期")
#     failure = models.IntegerField(verbose_name="失败数")
#     task_amount = models.DecimalField(max_digits=8,decimal_places=2,verbose_name="任务金额")
#     send_state = models.CharField(max_length=3,verbose_name="发送状态")
#     send_way = models.CharField(max_length=3,verbose_name="发送方式")
#     order_number = models.CharField(max_length=12,verbose_name="订单号")
#     user = models.CharField(max_length=50,verbose_name="用户")
#
#     class Meta:
#         db_table = "db_AiMarketing"
from oauth.models import CustomerInformation


class AutomateMessagePost(models.Model):
    customer = models.ForeignKey('CustomerLogin', models.DO_NOTHING, db_column='Customer_id', blank=True, null=True)  # Field name made lowercase.
    industry = models.CharField(db_column='Industry', max_length=255, blank=True, null=True)  # Field name made lowercase.行业
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.省份
    business_scope = models.CharField(db_column='Business_scope', max_length=255, blank=True, null=True)  # Field name made lowercase.经营范围
    filter = models.CharField(db_column='Filter', max_length=255, blank=True, null=True)  # Field name made lowercase.过滤已发送号码
    content = models.CharField(max_length=255, blank=True, null=True)#发送内容
    trade_name = models.CharField(db_column='Trade_name', max_length=255, blank=True, null=True)  # Field name made lowercase.#营销名称
    sending_time_setting = models.CharField(db_column='Sending_time_setting', max_length=255, blank=True, null=True)  # Field name made lowercase.发送时间
    amount = models.CharField(db_column='Amount', max_length=255, blank=True, null=True)  # Field name made lowercase.发送数量
    task_id = models.CharField(max_length=50)
    class Meta:

        db_table = 'Automate_message_post'


class AutomateMessageStatus(models.Model):
    customer = models.ForeignKey('CustomerLogin', models.DO_NOTHING, db_column='Customer_id', blank=True, null=True)  # Field name made lowercase.用户id
    amount = models.CharField(db_column='Amount', max_length=255, blank=True, null=True)  # Field name made lowercase.总数
    task_id = models.CharField(db_column='Task_id', max_length=255, blank=True, null=True)  # Field name made lowercase.任务id
    success = models.CharField(db_column='Success', max_length=255, blank=True, null=True)  # Field name made lowercase.成功
    unknow = models.CharField(db_column='Unknow', max_length=255, blank=True, null=True)  # Field name made lowercase.未知
    failed = models.CharField(db_column='Failed', max_length=255, blank=True, null=True)  # Field name made lowercase.失败


    class Meta:

        db_table = 'Automate_message_status'




class CustomerLogin(models.Model):
    customer_id = models.AutoField(db_column='Customer_id', primary_key=True)  # Field name made lowercase.用户id
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)  # Field name made lowercase.手机号
    name = models.CharField(db_column='Name', max_length=20, blank=True, null=True)  # Field name made lowercase.用户名
    identity_status = models.CharField(db_column='Identity_status', max_length=255, blank=True, null=True)  # Field name made lowercase用户认真状态
    administrator_status = models.CharField(db_column='Administrator_status', max_length=255, blank=True, null=True)  # Field name made lowercase.管理员状态

    class Meta:

        db_table = 'Customer_login'


class EnterpriseArticlesChannel(models.Model):
    """
    文章频道
    """
    name = models.CharField(max_length=10, verbose_name='频道名称')
    sequence = models.SmallIntegerField(verbose_name='组内顺序')
    class Mate:
        db_table = "Enterprise_channel"
        verbose_name = "触客频道"

class EnterpriseArticlesModel(models.Model):
    """
    文章详情
    """
    # title = models.CharField(max_length=50)
    image_url = models.CharField(max_length=250,null=True,blank=True)
    # video_url = models.CharField(max_length=250,null=True,blank=True)
    enterprise_type = models.ForeignKey(EnterpriseArticlesChannel,null=True,blank=True)
    content = models.CharField(max_length=3000)
    author = models.ForeignKey(CustomerInformation,max_length=100)
    enterprise = models.CharField(max_length=30)
    thumbs_up = models.SmallIntegerField(default=0)
    is_examine = models.BooleanField(default=False)
    is_recommend = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Mate:
        db_table = "Enterprise_articles"
        verbose_name = "触客分发"


class CommentsOnArticlesModel(models.Model):
    """
    文章评论
    """
    enterprise = models.CharField(max_length=50)
    thumbs_up = models.SmallIntegerField(default=0)
    content = models.CharField(max_length=150)
    mid = models.ForeignKey(CustomerInformation,max_length=100)
    is_examine = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True,null=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "Enterprise_comment"
        verbose_name = "评论"

class ThumbsUpModel(models.Model):
    """
    点赞
    """
    thumbs_up_type = models.SmallIntegerField(verbose_name="点赞类型")
    cover_mid = models.IntegerField()
    up_mid = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True,null=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "Enterprise_Thumbs_Up"
        verbose_name = "点赞记录"

class ArticleResponseModel(models.Model):
    comment = models.ForeignKey(CommentsOnArticlesModel,max_length=100)
    reply_id = models.CharField(max_length=50)
    mid = models.CharField(max_length=50)
    content = models.CharField(max_length=150)
    to_mid = models.CharField(max_length=50)

    class Meta:
        db_table = "Enterprise_response"
        verbose_name = "评论回复"