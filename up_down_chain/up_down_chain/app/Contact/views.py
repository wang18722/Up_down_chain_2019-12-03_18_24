import math

import time

import pickle


from Contact.models import AutomateMessageStatus, AutomateMessagePost
from celery_tasks.sms.tasks import send_sms_code
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from Enterprise.utils import value
# from Industry.views import PreciseRetrievalView
from Enterprise.models import *
from django_redis import get_redis_connection
import re
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin,RetrieveModelMixin
from rest_framework.response import Response
from up_down_chain.utils.qiniuyun.qiniu_storage import storage
from up_down_chain.utils.page import StandardPageNumberPagination
from .serializables import   ObtainTouchArticleSerializer,TouchArticleSerializer,CommentsOnArticlesSerializer, \
    ThumbsUpSerializer
from .models import EnterpriseArticlesModel,CommentsOnArticlesModel
from django.conf import settings


class ManualMarketingView(APIView):
    """手动营销(手动发信息)"""
    pass
    # def post(self, request):
    #     # 1.获取data数据
    #     body_data = request.data
    #     # 连接redis
    #     conn = get_redis_connection("sms_code")
    #     # 2.解析出Mobile, content, username, a_number
    #     content = body_data["content"]
    #     username = body_data["username"]
    #     a_number = body_data["a_number"]
    #
    #     # 5.截取出mobile一百个号码每组字符串发送, 截止发送完毕(考虑mobile是否在redis中取出)
    #     user_mobile = pickle.loads(conn.get("sms_code"))
    #     # 取出所有号码
    #     mobile = user_mobile["mobile"]
    #
    #     # 截取出mobile一百个号码每组字符串发送, 截止发送完毕
    #     list_mobile = mobile.split(",")
    #     # 列表的长度
    #     mobile_count = len(list_mobile)
    #
    #     # 将手机号数量和发送条数*手机号存储数量
    #     count_dict = {}
    #     count_dict["mobile_count"] = mobile_count
    #     count_dict["send_count"] = int(a_number) * mobile_count
    #     count_dict["user"] = User.objects.filter(username=username).first().id
    #     serializer = RecordSerializer(data=count_dict)
    #     if serializer.is_valid():
    #         serializer.save()
    #
    #     else:
    #         return Response(serializer.errors)
    #
    #     start = 0
    #
    #     while start < mobile_count:
    #         # 切片列表 每组为100
    #         new_liat = list_mobile[start:start + 4]
    #         try:
    #             # 查询数据库中用户对应的那个余额表
    #             balance_obj = Top_up_Payment.objects.filter(
    #                 id=User.objects.filter(username=username).first().id).first().balance
    #             print(balance_obj)
    #
    #         except:
    #             return Response({"massage": "用户不存在"})
    #         # 3.判断a_number(条数)是否大于1或等于1 1 < 条数 * 0.35*号码数量   条数 = 1 * 0.35*号码数量
    #         if a_number == 1:
    #             try:
    #                 # 余额数据计算
    #                 balance_obj = float('%.2f' % balance_obj)
    #                 num = float('%.2f' % (len(new_liat) * 0.035))
    #
    #                 # 余额
    #                 balance = balance_obj - num
    #                 balance = round(balance, 2)
    #                 if balance < 0:
    #                     return Response({'lack_balance': 0})
    #                 id_num = User.objects.filter(username=username).first().id
    #                 # print(111111)
    #                 # 查询对象
    #                 obj = Top_up_Payment.objects.filter(userid_id=id_num)
    #                 balance_dict = {}
    #                 balance_dict["balance"] = balance
    #                 # 更新余额
    #                 serializer = Top_upSerializer(obj, data=balance_dict, partial=True)
    #
    #                 if serializer.is_valid():
    #                     serializer.save()
    #
    #                 else:
    #                     return Response(serializer.errors)
    #             except:
    #                 # 返回余额不足
    #                 return Response({"massage": "程序出错"})
    #
    #         # 4.认证企业对应的金额减条数 * 0.35, 并更新数据库余额!如果余额不足则返回去充值
    #
    #         try:
    #             # 余额数据计算
    #             balance_obj = float('%.2f' % balance_obj)
    #             num = float('%.2f' % (len(new_liat) * int(a_number) * 0.035))
    #
    #             # 余额
    #             balance = balance_obj - num
    #             balance = round(balance, 2)
    #             if balance < 0:
    #                 return Response({'lack_balance': 0})
    #
    #             # 查询用户id
    #             id_num = User.objects.filter(username=username).first().id
    #             # print(111111)
    #             # 查询对象
    #             obj = Top_up_Payment.objects.filter(userid_id=id_num)
    #             # print(obj)
    #
    #             balance_dict = {}
    #             balance_dict["balance"] = balance
    #             # print(balance_dict)
    #
    #             # 更新余额
    #             serializer = Top_upSerializer(obj, data=balance_dict, partial=True)
    #             # print(serializer)
    #             # 保存数据
    #             if serializer.is_valid():
    #                 serializer.save()
    #             else:
    #                 return Response(serializer.errors)
    #         except:
    #             # 返回余额不足
    #             return Response({"massage": "程序出错"})
    #         # 列表转字符串
    #         str_mobile = ','.join(new_liat)
    #         print(str_mobile)
    #
    #         # 使用celery发送短息
    #         dict_aa = {}
    #         dict_aa["contents"] = content
    #         dict_aa["username"] = username
    #         send_sms_code.delay(str_mobile, dict_aa)
    #
    #         start = start + 4
    #
    #         # 6.返回结果
    #
    #     return Response({"massage": "ok"})


# class RetrievingTargetLibrary(PreciseRetrievalView):
#     """此功能继承首页精准搜索功能"""
#     pass


class AiMarketingView(APIView):
    """保存精准自动AI营销设置"""

    # 测试数据
    # "industry":1,
    # "main":"农业",
    # "provinces":["广东省","广西省","湖南省"],
    # "time":"12:00",
    # "limited":100,
    # "username":1,
    # "trade_name":"为人投资招标信息",
    # "content":"中国模范企业为人公司招标投资信息"

    def post(self, request):
        data = request.data
        print(data)
        # 1.获取对应省份的总数电话号码
        conn = get_redis_connection("sms_code")
        i = value(data["industry"])
        # print(i)
        #     1.1查询对应的行业，省份，模糊查询主营信息
        mobile_list = []
        try:
            # 处理多个省份
            for province in data["provinces"]:
                # print(province)

                obj_data = globals()[i].objects.filter(province=province, industry_involved=data["main"])

                for obj in obj_data:
                    mobile = obj.phone
                    # 2.对电话号码进行处理，只发手机号
                    if not mobile == None:
                        #     2.1用正则提取手机号
                        mobile = re.match(r"1[0-9]\d{9}$", mobile)
                        if not mobile == None:
                            mobile_list.append(mobile.group(0))

        except:
            return Response({"message": "查询出错"})
        # print(mobile_list)

        # 计算时间
        time_num = len(mobile_list) / data["limited"]
        int_time_num = math.ceil(time_num)
        # 3.按用户限定的条数做分批
        n = 0
        while n < len(mobile_list):
            # 每批数据
            list_data = mobile_list[n:n + data["limited"]]

            # 4.处理多少天的分批任务，保证每天批号不一样，可用单号标记
            order_no = str(time.strftime('%Y%m%d', time.localtime(time.time()))) + str(time.time()).replace('.', '')[
                                                                                   -7:]

            obj = AutomateMessagePost()

            obj.task_id = order_no  # 单号
            obj.industry = data["industry"]  # 行业
            obj.province = data["provinces"]  # 省份
            obj.business_scope = ""  # 经营范围
            obj.filter = list_data
            obj.content = data["content"]  # 发送内容
            obj.trade_name = data["trade_name"]  # 营销名称
            obj.sending_time_setting = data["time"]  # 发送时段
            obj.amount = data["limited"]  # 发送数量
            obj.customer = data["username"]  # 发送数量
            print(obj)
            # obj.commit()
            obj.save()

            # conn.set(data["username"]+order_no,list_data,int_time_num*24*60*60)


            # 是发送了再保存还是设置的时候保存




            n += data["limited"]
        print(1111111111)

        # 5.获取需要发送的时间段

        # 6.处理每天时间段发送的单号，实现定时发送



class TouchArticlesViews(GenericAPIView,UpdateModelMixin):
    serializer_class = TouchArticleSerializer
    queryset = EnterpriseArticlesModel.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
        except Exception as e:
            user = None
        if user and request.user.is_authenticated:
            image_list = request.data.getlist('image_url')
            image_list_url = []
            image_num = 0
            if len(image_list) > 9:
                return Response({
                    'message': "图片超出限制"
                })

            # 后期开启

            # from celery_tasks.qiniu.qiniu import send_storage
            for image in image_list:
                if re.search("w*\\.(mp4|rmvb|flv|mpeg|avi)", image._name):
                    image_num += 1
                if image_num > 1:
                    return Response({
                        'message': "只可以上传一个视频"
                    })

                image_parameter = storage(image.read())
                image_list_url.append(settings.QINIUYUN_URL + image_parameter)

            # 图片地址
            request.data['image_url'] = str(image_list_url)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response({
                "message": "未授权",
            })

class ObtainTouchArticlesViews(GenericAPIView,RetrieveModelMixin):
    """
    获取单篇文章内容
    """
    serializer_class = ObtainTouchArticleSerializer
    queryset = EnterpriseArticlesModel.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)


class CommentsOnArticlesViews(GenericAPIView,CreateModelMixin):
    """
    评论显示
    """
    serializer_class = CommentsOnArticlesSerializer
    pagination_class = StandardPageNumberPagination

    def post(self, request, *args, **kwargs):
        """评论保存"""
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """评论获取"""
        queryset = CommentsOnArticlesModel.objects.filter(enterprise=request.query_params['enterprise']).order_by('create_time')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ThumbsUpViews(GenericAPIView):
    serializer_class = ThumbsUpSerializer

    def post(self,request, *args, **kwargs):
        if request.data['status_model'] == 'Article':
            Comments = EnterpriseArticlesModel.objects.get(id=request.data['pk'])
        else:
            Comments = CommentsOnArticlesModel.objects.get(id=request.data['pk'])

        Comments.thumbs_up = Comments.thumbs_up + 1
        Comments.save()

        return Response({"message": "OK"})

    def put(self,request, *args, **kwargs):
        """评论点赞"""
        pass