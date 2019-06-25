# from apscheduler.schedulers.blocking import BlockingScheduler
#
# from datetime import datetime
# # 当前时间
# print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
# def job():
#     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
# scheduler = BlockingScheduler()
# scheduler.add_job(job,'cron',day_of_week = "1-5",hour = 6,minute = 30)
# print("正在启动")
# scheduler.start()
import time
from datetime import date


def get_order_code():
    order_no = str(time.strftime('%Y%m%d', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
    print(order_no)
    return order_no
get_order_code()

