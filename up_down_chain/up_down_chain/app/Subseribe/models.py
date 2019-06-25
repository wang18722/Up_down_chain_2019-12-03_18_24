from django.db import models

from Enterprise.models import Provinces
from oauth.models import CustomerInformation


class Bids(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    Title = models.CharField(db_column='Title', max_length=300, blank=True,
                             null=True)  # Field name made lowercase.
    BidsPirce = models.CharField(db_column='BidsPrice', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    Company = models.CharField(db_column='Company', max_length=200, blank=True,
                               null=True)  # Field name made lowercase.
    Url = models.CharField(db_column='Url', max_length=200, blank=True, null=True)  # Field name made lowercase.
    Source = models.CharField(db_column='Source', max_length=200, blank=True,
                              null=True)  # Field name made lowercase.
    ReleaseDate = models.CharField(db_column='ReleaseDate', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    StartDate = models.CharField(db_column='StartDate', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    EndDate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    BidsAreaID = models.CharField(db_column='BidsAreaID', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    IsValid = models.IntegerField(db_column='IsValid', blank=True, null=True)  # Field name made lowercase.
    IsDeleted = models.IntegerField(db_column='IsDeleted', blank=True, null=True)  # Field name made lowercase.
    CreateTime = models.DateField(db_column='CreateTime',auto_now_add=True)  # Field name made lowercase.
    BidsContent = models.TextField(db_column='BidsContent', blank=True, null=True)  # Field name made lowercase.
    Phone = models.CharField(db_column="Phone",null=True,blank=True,max_length=100)

    class Meta:
        db_table = 'web_bids'
        verbose_name = "文章表"
        verbose_name_plural = verbose_name




class BidsUserSetting(models.Model):
    """
    用户订阅表
    """

    mid = models.ForeignKey(CustomerInformation,null=True, on_delete=models.CASCADE, verbose_name="用户")
    areas_id = models.CharField(max_length=60, verbose_name="关注省范围")
    keywords_array = models.CharField(max_length=60, verbose_name="关注关键字")
    # by_time = models.TimeField(null=True,verbose_name="截止时间")
    remind_long_time = models.SmallIntegerField(default=7, verbose_name="推送时常")
    is_remind = models.BooleanField(default=True, verbose_name="是否推送")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "Subscribe_status"
        verbose_name = "推送用户记录表"
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
