from django_redis import get_redis_connection

from celery_tasks.main import app
from up_down_chain.libs.xiangxun.smsSDK import REST


@app.task(name='send_sms_code')
def send_sms_code(mobile,data):
    """celery异步发送短信"""

    ccp = REST()
    print(mobile)
    print(data)
    ccp.run(mobile,data)
