from Pays.models import RechargeModel
from Subseribe.models import BidsUserSetting
import redis

def update():
    """设置使用数"""
    short_message_num = RechargeModel.objects.count()
    subscribe_num = BidsUserSetting.objects.count()
    touches_num = 1565
    redis_client = redis.Redis(host="127.0.0.1",port=6379,db=5)
    redis_client.mset(short_message_num=short_message_num,subscribe_num=subscribe_num,touches_num=touches_num)

    return "OK"
