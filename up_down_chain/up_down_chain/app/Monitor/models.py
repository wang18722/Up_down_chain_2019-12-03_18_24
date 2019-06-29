from django.db import models

# Create your models here.

class MonitorsInfo(models.Model):
    """监控后台模型类"""
    url = models.CharField(max_length=100,verbose_name="被访问的url")
    userid = models.CharField(max_length=10,verbose_name="用户id")
    username = models.CharField(max_length=10,verbose_name="用户名字")
    city = models.CharField(max_length=20,verbose_name='城市',null=True)
    province = models.CharField(max_length=20,verbose_name='省份',null=True)
    headimgUrl = models.CharField(max_length=200,verbose_name='头像url',null=True)
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "db_MonitorsInfo"
        verbose_name = "监控后台信息表"