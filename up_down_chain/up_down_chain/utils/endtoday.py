import datetime
import time

def rest_of_day():
    """
    :return: 截止到目前当日剩余时间
    """
    today = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
    tomorrow = today + datetime.timedelta(days=1)
    nowTime = datetime.datetime.now()

    return (tomorrow - nowTime).seconds  # 获取秒






# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def Caltime(begin_time):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    # date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    # date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")

    date1 = time.strptime(begin_time, "%Y-%m-%d").tm_yday
    date2 = time.strptime(str(datetime.date.today()), "%Y-%m-%d").tm_yday


    # 返回两个变量相差的值，就是相差天数
    return date2 - date1


