from django.db import models

class Area(models.Model):
    """
    推送地区
    """
    name = models.CharField(max_length=50,verbose_name="省名称")
    isDeleted = models.BooleanField(default=False,verbose_name="是否删除")

    class Meta:
        db_table = "up_area"
        verbose_name = "地区"
        verbose_name_plural = verbose_name

