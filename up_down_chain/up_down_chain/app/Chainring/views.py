from json import load

import random

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from jieba import xrange
from rest_framework.generics import GenericAPIView, UpdateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.views import APIView

from Chainring.models import Associated, Grouping
from rest_framework.response import Response

from Chainring.serializables import GroupingSerializer, AssociatedSerializer, EnterpriseSerializer
from oauth.models import CustomerInformation


class ChainRingView(GenericAPIView):
    """首页信息展示"""
    serializer_class = GroupingSerializer

    def get(self, request):
        username = request.GET.get("username")
        print(username)

        try:
            # 查询用户对应的企业的分组信息
            user_data = CustomerInformation.objects.filter(username=username).first()
        except:
            return Response({"massage": "查询出错"})
        data_list = []
        # 判断该用户是否有认证企业
        if user_data.certification == True:

            # 查询用户对应关注表的信息
            grouping = Associated.objects.filter(userid_id=user_data.id).filter()
            print(grouping)
            # 遍历所有对象
            for index in range(len(grouping)):
                print(index)
                # 查询企业对应 的分组信息
                grouping_data = Grouping.objects.filter(id=grouping[index].groupingid_id).filter()
                print(grouping_data)
                for i in grouping_data:
                    data_list.append(i)

            # 去从
            new_liat = set(data_list)
            print(new_liat)
            # 如果没关注有企业则返回空
            if new_liat == set():
                return Response({"massage": "该用户没关注有企业"})

            serializer = GroupingSerializer(new_liat, many=True)
            return Response(serializer.data)


        else:
            return Response({"massage": "你还没认证企业,请去认证"})


class FocusView(ListCreateAPIView, UpdateAPIView):
    """
    加关注
    """

    # serializer_class = AssociatedSerializer
    def get(self, request, *args, **kwargs):
        """点击搜索功能"""
        # 获取用户输入的关键字
        data = request.GET.get("data")
        # 连接redis
        conn = get_redis_connection("default")
        # 判断是否为空,空则返回特定数据
        enterprise_data = 企业.objects.all()
        print(type(enterprise_data))
        enterprise_count = 企业.objects.count()
        if data == None:
            import pickle
            # 将数据放进 rides,注意存进的格式
            conn.set("count_data", pickle.dumps(enterprise_data))  # 注  data中需要更换用户的名字

            # 获取数据并解码
            redis_data = conn.get("count_data")  # .decode()
            redis_data = pickle.loads(redis_data)
            # 随机返回3条数据
            sample = random.sample(xrange(enterprise_count), 3)
            print(sample)
            result = [redis_data[i] for i in sample]
            print(result)
            serializer = EnterpriseSerializer(list(result), many=True)
            return Response(serializer.data)

        else:
            # 如果有数据则进行模糊插叙返回数据
            all_data = 企业.objects.filter(enterprises__contains=data).filter()
            serializer = EnterpriseSerializer(all_data, many=True)
            return Response(serializer.data)

    def patch(self, request, *args, **kwargs):

        body_data = request.data
        print(body_data)
        focus = body_data["focus"]

        try:
            # 查询用户所对用的id
            user_id = User.objects.filter(username=body_data["username"]).first().id
            # 查询用户对应的企业
            enterprises_id = 企业.objects.filter(enterprises=body_data["enterprises"]).first().id
            grouping_id = Grouping.objects.filter(grouping=body_data["grouping"]).first().id

        except:
            return Response()
        # 查询请求的数据,数据库有没有存在
        ass_obj = Associated.objects.filter(userid_id=user_id, enterprisesid_id=enterprises_id).filter()
        if ass_obj:

            serializer = AssociatedSerializer(ass_obj, data=body_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.validated_data)

            else:
                return Response(serializer.errors)

        elif focus == 1:

            # 获取对象 保存新数据
            new_obj = Associated()
            new_obj.focus = focus
            new_obj.userid_id = user_id
            new_obj.enterprisesid_id = enterprises_id
            new_obj.groupingid_id = grouping_id
            # 保存操作
            new_obj.save()
            print(111)

        return Response({"massage": "操作成功"})
