from django.db import models

class BaseModel(models.Model):
    #模型基类
    create_time = models.DateField(verbose_name="创建时间",auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="创建时间",auto_now=True)

    class Meta:
        abstract = True #声明一个抽象类,只用于继承,不会在数据库创建对应的表