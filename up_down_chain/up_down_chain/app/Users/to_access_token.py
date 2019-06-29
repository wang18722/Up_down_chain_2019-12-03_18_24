from wechatpy.client import WeChatClient
import os, django
from django.conf import settings
import redis
import time

def get_access_token():
    # print(1)
    redis_client = redis.Redis(host="127.0.0.1",port=6379,db=5)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "up_down_chain.settings")  # project_name 项目名称
    django.setup()

    wechat_client = WeChatClient(
        settings.WXAPPID,
        settings.WXAPPSECRET,

    )
    access_token = wechat_client.fetch_access_token()["access_token"]
    time.sleep(5)
    redis_client.setex("access_token",access_token,7000)


    return "ok"

