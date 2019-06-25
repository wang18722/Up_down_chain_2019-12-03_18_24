from celery import Celery

# 为celery使用django配置文件进行设置
import os
print(os)

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = "up_down_chain.settings"

# 创建celery应用
app = Celery('up_down_chain')

# 导入celery配置
app.config_from_object('celery_tasks.conf')

# 自动注册celery任务
app.autodiscover_tasks(['celery_tasks.sms'])

# celery -A celery_tasks.main worker -l info