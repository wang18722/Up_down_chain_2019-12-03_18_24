# import datetime
# def get_date(days=7):
#     return datetime.datetime.now() - datetime.timedelta(days=days)
# print(get_date())
# 取得当前时间戳
import time
print(time.time())
# 格式化时间戳为标准格式
print(time.strftime('%Y.%m.%d',time.localtime(time.time())))
# 获取30天前的时间（通过加减秒数来获取现在或者未来某个时间点）
print(type(time.strftime('%Y-%m-%d',time.localtime(time.time()-2592000))))
