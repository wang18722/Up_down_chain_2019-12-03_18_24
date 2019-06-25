

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间',default=timezone.now
)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True