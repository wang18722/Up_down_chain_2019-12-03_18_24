from wechatpy.client import WeChatClient
import os, django
from up_down_chain import settings
import redis
import time
def get_access_token():
    try:
        redis_client = redis.Redis(host="127.0.0.1",port=6379,db=5)


        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "up_down_chain.settings")  # project_name 项目名称
        django.setup()
        wechat_client = WeChatClient(
            settings.WXAPPID,
            settings.WXAPPSECRET,

        )
        redis_client.setex("access_token",wechat_client.fetch_access_token()["access_token"],7000)
        time.sleep(5)
    except Exception as e:
        print(e)
    return "ok"

# print(get_access_token())


