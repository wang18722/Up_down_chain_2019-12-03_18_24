import pickle

from django.shortcuts import render

# Create your views here.

from datetime import datetime

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from oauth.models import CustomerInformation

# '河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','海南','四川','贵州','云南','陕西','甘肃','青海','台湾',
# '北京','天津','上海','重庆','内蒙古','广西','宁夏','新疆','西藏','香港','澳门',


class MonitorUserView(RetrieveAPIView):
    """后台监控"""
    """
    埋点位置：
    首页，发送，企业认证，订阅推送,充值
    """
    """
    如果在用户登录的位置加一个中间件
    """
    def get(self, request, *args, **kwargs):
        # token = jwt_decode_handler(request.GET["token"])
        # print(token)
        # 1.封装一个函数，用于检测各个url
        # monitor(token)

        conn = get_redis_connection("monitor")
        # conn_province = get_redis_connection("province_data")
        redis_data = conn.keys()

        try:
            #1.获取用户总数，查询用户表
            all_count = CustomerInformation.objects.filter().count()
            #2.获取redis总数为在线用户数
            online_count = len(redis_data)
            #3.使用今天时间节点查询用户表获取今日新增
            today = datetime.now().strftime("%Y-%m-%d")
            today_add_count = CustomerInformation.objects.filter(CreateTime=today).count()
            #返回的数据
        except:
            return Response({"message":"系统崩溃"})
    #     province_list = conn_province.get("data")
    #
    #     if not province_list:
    #         province_list = []
    #         all_province=['河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽',
            # '福建','江西','山东','河南','湖北','湖南','广东','海南','四川',
            # '贵州','云南','陕西','甘肃','青海','台湾',
    # '北京','天津','上海','重庆','内蒙古','广西','宁夏','新疆','西藏','香港','澳门']
    #         for province in all_province:
    #             province_dict = {}
    #             count = CustomerInformation.objects.filter(city__startswith = province).count()
    #
    #             province_dict[province] = count
    #             province_list.append(province_dict)
    #         conn_province.set("data",pickle.dumps(province_list),60)
    #         print(111)
    #         # conn_province.hset("data",province_list,600)
    #
    #         # 处理身份数据
    #         info_data = {
    #             "all_count": all_count,
    #             "online_count": online_count,
    #             "today_add_count": today_add_count,
    #             "province_count": province_list
    #         }
    #         # 3.将数据获取到
    #         return Response(info_data)

        # 处理身份数据
        info_data = {
            "all_count":all_count,
            "online_count":online_count,
            "today_add_count":today_add_count,
            # "province_count":pickle.loads(province_list)
        }

    # 3.将数据获取到
        return Response(info_data)

class OnlineUserView(RetrieveAPIView):
    """在线用户"""
    def get(self, request, *args, **kwargs):
        """省份"""
        province = request.GET["province"]
        conn = get_redis_connection("monitor")
        redis_data = conn.keys()

        # 获取每条数据
        # 定义列表存放数据
        list_data = []
        for i in redis_data:
            # 解析出数据

            data = conn.get(i).decode()
            data = eval(data)

            if data:
                if province =="全国":
                    dict_data = {}
                    dict_data["city"] = data["city"]
                    dict_data["username"] = data["username"]
                    dict_data["headimgUrl"] = data["headimgUrl"]
                    dict_data["province"] = data["province"]
                    list_data.append(dict_data)



                if data["province"]== province:
                    dict_data = {}
                    dict_data["city"] = data["city"]
                    dict_data["username"] = data["username"]
                    dict_data["headimgUrl"] = data["headimgUrl"]
                    dict_data["province"] = data["province"]
                    list_data.append(dict_data)
                    print(dict_data)



        #需要返回的数据
        info_data = {
            "user_info_data":list_data,

            "count":len(list_data),


        }

        return Response(info_data)