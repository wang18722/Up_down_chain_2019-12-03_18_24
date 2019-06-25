from django.db import models

from Enterprise.models import Enterprises

# Create your models here.
from Users.models import EnterpriseCertificationInfo


class Grouping(models.Model):
    """分组表"""
    grouping = models.CharField(max_length=128, verbose_name="分组名称")

    class Meta:
        db_table = 'db_Grouping'
        verbose_name = "分组信息表"

    def __str__(self):
        return self.grouping



class Associated(models.Model):
    """关联表"""
    focus = models.BooleanField(verbose_name="是否关注", default=False)
    enterprisesid = models.ForeignKey(Enterprises, on_delete=models.CASCADE)
    userid = models.ForeignKey(EnterpriseCertificationInfo, on_delete=models.CASCADE)
    groupingid = models.ForeignKey(Grouping, on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_Associated'
        verbose_name = "中间表"

    # def __str__(self):
    #     return self.focus



# class EnterpriseModel(models.Model):
#     """企业表"""
#     enterprises = models.CharField(max_length=128, verbose_name="企业")
# #     provinces = models.CharField(max_length=128, verbose_name="省份")
#
#
#
#     class Meta:
#         db_table = 'db_EnterpriseModel'
#         verbose_name = "企业信息表"
#
#     def __str__(self):
#         return self.enterprises
#
# class User(models.Model):
#     """用户表"""
#     username = models.CharField(max_length=30, verbose_name="用户")
#     mobile = models.CharField(max_length=11, verbose_name='手机号')
#     certification = models.BooleanField(verbose_name="是否认证", default=False)
#     cid = models.ManyToManyField(EnterpriseModel)
#
#     class Meta:
#         db_table = 'db_Grouping'
#         verbose_name = "用户表"
#
#     def __str__(self):
#         return self.username
