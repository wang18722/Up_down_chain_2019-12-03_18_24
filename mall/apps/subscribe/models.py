from django.db import models
from areas.models import Area
from utils.models import BaseModel


class Bids(BaseModel):
    """
    文章表
    """
    title = models.CharField(max_length=100,verbose_name="标题")
    pirce = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    company = models.CharField(max_length=100,verbose_name="公司")
    url = models.CharField(max_length=200,verbose_name="地址")
    source = models.CharField(max_length=100,verbose_name="来源")
    areas_id = models.ForeignKey(Area,on_delete=models.PROTECT, related_name='province_addresses',verbose_name="地区")
    content = models.TextField(default=None,null=True,blank=True,verbose_name="文章内容")
    isValid = models.BooleanField(default=True,verbose_name="是否有效")
    isDeleted = models.BooleanField(default=False,verbose_name="是否删除")
    # areas_id = models.SmallIntegerField(verbose_name="地区地址")
    by_time = models.DateField(verbose_name="截止时间",auto_now_add=True,null=True)
    class Meta:
        db_table = "up_bids"
        verbose_name = "文章表"
        verbose_name_plural = verbose_name



class BidsUserSetting(BaseModel):
    """
    用户订阅表
    """
    REMIND_TIME_ENUM = {
        "WEEK": 1,
        "MONTH": 2,
    }

    REMIND_TIME_CHOICES = (
        (1, 7),
        (2, 30),
        (3, 90),
    )
    # mid = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user",verbose_name="用户")
    areas_id = models.CharField(max_length=60,verbose_name="关注省范围")
    keywords_array = models.CharField(max_length=60,verbose_name="关注关键字")
    by_time = models.TimeField(null=True,verbose_name="截止时间")
    remind_long_time = models.SmallIntegerField(choices=REMIND_TIME_CHOICES,default=1,verbose_name="推送时常")
    is_remind = models.BooleanField(default=True,verbose_name="是否推送")

    class Meta:
        db_table = "up_user_bids_setting"
        verbose_name = "推送用户记录表"
        verbose_name_plural = verbose_name

class User(models.Model):
    """
    用户表
    """
    neme = models.CharField(max_length=30,null=True,verbose_name="用户名")
    image_url = models.CharField(max_length=200,verbose_name="t头像图片")
    bids_set_id = models.ForeignKey(BidsUserSetting,on_delete=models.SET_DEFAULT,null=True,blank=True,default=None,related_name="bidset",verbose_name="订阅表")
    article = models.ManyToManyField(Bids,related_name="collections")
    class Meta:
        db_table = "up_user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name


# class ArticledetailModel(models.Model):
#     """
#     文章关注表
#     """
#     # focus = models.BooleanField(verbose_name="是否关注", default=False)
#     mid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", verbose_name="用户")
#     bids_id = models.ForeignKey(Bids, on_delete=models.CASCADE,default=None,related_name="bidset", verbose_name="订阅表")
#
#     class Meta:
#         db_table = "up_bids_user_follow"
#         verbose_name = "文章关注表"
#         verbose_name_plural = verbose_name