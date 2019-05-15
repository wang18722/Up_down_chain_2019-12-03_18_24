from celery import Celery

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings'

#创建Celery对象
#参数main 设置脚本名
app = Celery('celery_tasks')

#加载配置文件
app.config_from_object('celery_tasks.config')
app.autodiscover_tasks(['celery_tasks.remind'])