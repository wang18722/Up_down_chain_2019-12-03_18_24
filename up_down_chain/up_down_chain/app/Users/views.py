import hashlib
import os
import pickle
import random
import re
from datetime import datetime
from macpath import join
# Create your views here
from decimal import Decimal
from PIL import Image
from django_redis import get_redis_connection
from jieba import xrange
from mutagen._util import get_size
from rest_framework.generics import UpdateAPIView, ListCreateAPIView, CreateAPIView, GenericAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_decode_handler

from Enterprise.utils import value
from Users.models import Top_up_Payment, EnterpriseCertificationInfo, ManualMessagePost, Template
from Users.serializables import Top_upSerializer, RecordSerializer, TemplateSerializer, ManualMessagePostSerializer, \
    EnterpriseCertificationSerializer, SaveOrderSerializer, MoenyUpdateSerializer, UpdateTemplateSerializer, \
    GetTemplateSerializer, AuthenticationAuditTemplateSerializer, PayCertificationSerializer
from celery_tasks.sms.tasks import send_sms_code
import time
from Industry.models import *

from oauth.models import CustomerInformation
from up_down_chain.utils.payment import get_pay_info
from up_down_chain.utils.send_template import Send_template

class EnterpriseCertificationView(CreateAPIView):
    """企业认证"""

    def create(self, request, *args, **kwargs):

        data = request.data
        # print(data)
        token = jwt_decode_handler(data["token"])
        print(token)
        user = token["user_id"]
        data["user"] = user
        # 生成哈希company_id
        m = hashlib.md5()
        company_name = data["name"]
        m.update(company_name.encode())
        # 企业id
        company_id = m.hexdigest()
        data["company_id"] = company_id
        try:
            obj_en = EnterpriseCertificationInfo.objects.filter(company_id=company_id)
            obj_user = EnterpriseCertificationInfo.objects.filter(user=user)
        except:
            return Response({"message": "查询出错"})
        if obj_en:
            return Response({"message": "该企业已经认证"})
        if obj_user:
            return Response({"message": "用户已经认证企业"})
        # 图片压缩处理
        try:
            image = request.FILES["avatar"]
        except:
            return Response({"message": "图片错误"})
        # 获取图片大小
        o_size = get_size(image)
        quality = 90
        step = 5
        # 处理图片名称
        data_time = datetime.now().strftime("%Y%m%d%H")
        image_name = data_time + company_name + "." + image.name.split(".")[-1]

        # 图片路径
        path = "/home/python/Desktop/Up_down_chain/up_down_chain/static/" + image_name

        if o_size <= 40000:
            im = Image.open(image)
            im.save(path, quality=quality)
            data["avatar"] = image_name

            serializer = EnterpriseCertificationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"code":0})

            else:
                return Response(serializer.errors)

        # path=""
        # 图片压缩
        while o_size > 400000:
            im = Image.open(image)
            im.save(path, quality=quality)

            if quality - step < 0:
                break
            quality -= step
            o_size = os.path.getsize(path)

        data["avatar"] = image_name
        serializer = EnterpriseCertificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        else:
            return Response(serializer.errors)

        return Response({"code": 0})

class SmsCodeView(UpdateAPIView):
    """
        发送短信

        测试数据:conn.set("sms_code",pickle.dumps({"mobile":"13612238280,18620885204,18927522512,15576502492,19875861808,13723441396,17375525590,18738512271,18926259234,18998358234,18926165234,18998310234,18922789834,18922165834,18929567834,18922765834,13926293516,18903071677,15089677014"}))


    """

    def post(self, request):
        # 1.获取data数据
        body_data = request.data
        # 连接redis
        conn = get_redis_connection("sms_code")
        # 2.解析出Mobile, content, username, a_number
        content = body_data["content"]
        user_id = body_data["user_id"]
        a_number = body_data["a_number"]

        # 5.截取出mobile一百个号码每组字符串发送, 截止发送完毕(考虑mobile是否在redis中取出)
        user_mobile = pickle.loads(conn.get("sms_code"))
        # 取出所有号码
        mobile = user_mobile["mobile"]

        # 截取出mobile一百个号码每组字符串发送, 截止发送完毕
        list_mobile = mobile.split(",")
        # 列表的长度
        mobile_count = len(list_mobile)

        # 将手机号数量和发送条数*手机号存储数量
        count_dict = {}
        count_dict["mobile_count"] = mobile_count
        count_dict["send_count"] = int(a_number) * mobile_count
        count_dict["user"] = EnterpriseCertificationInfo.objects.filter(user=user_id,identity_status=2).first().id
        serializer = RecordSerializer(data=count_dict)
        if serializer.is_valid():
            serializer.save()

        else:
            return Response(serializer.errors)

        start = 0

        while start < mobile_count:
            # 切片列表 每组为100
            new_liat = list_mobile[start:start + 4]
            try:
                # 查询数据库中用户对应的那个余额表
                balance_obj = Top_up_Payment.objects.filter(
                    id=EnterpriseCertificationInfo.objects.filter(user=user_id,identity_status=2).first().id).first().balance
                print(balance_obj)

            except:
                return Response({"massage": "用户不存在"})
            # 3.判断a_number(条数)是否大于1或等于1 1 < 条数 * 0.35*号码数量   条数 = 1 * 0.35*号码数量
            if a_number == 1:
                try:
                    # 余额数据计算
                    balance_obj = float('%.2f' % balance_obj)
                    num = float('%.2f' % (len(new_liat) * 0.035))

                    # 余额
                    balance = balance_obj - num
                    balance = round(balance, 2)
                    if balance < 0:
                        return Response({'lack_balance': 0})
                    id_num = EnterpriseCertificationInfo.objects.filter(user=user_id,identity_status=2).first().id
                    # print(111111)
                    # 查询对象
                    obj = Top_up_Payment.objects.filter(userid_id=id_num)
                    balance_dict = {}
                    balance_dict["balance"] = balance
                    # 更新余额
                    serializer = Top_upSerializer(obj, data=balance_dict, partial=True)

                    if serializer.is_valid():
                        serializer.save()

                    else:
                        return Response(serializer.errors)
                except:
                    # 返回余额不足
                    return Response({"massage": "程序出错"})

            # 4.认证企业对应的金额减条数 * 0.35, 并更新数据库余额!如果余额不足则返回去充值

            try:
                # 余额数据计算
                balance_obj = float('%.2f' % balance_obj)
                num = float('%.2f' % (len(new_liat) * int(a_number) * 0.035))

                # 余额
                balance = balance_obj - num
                balance = round(balance, 2)
                if balance < 0:
                    return Response({'lack_balance': 0})

                # 查询用户id
                id_num = EnterpriseCertificationInfo.objects.filter(user=user_id,identity_status=2).first().id
                # print(111111)
                # 查询对象
                obj = Top_up_Payment.objects.filter(userid_id=id_num)
                # print(obj)

                balance_dict = {}
                balance_dict["balance"] = balance
                # print(balance_dict)

                # 更新余额
                serializer = Top_upSerializer(obj, data=balance_dict, partial=True)
                # print(serializer)
                # 保存数据
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors)
            except:
                # 返回余额不足
                return Response({"massage": "程序出错"})
            # 列表转字符串
            str_mobile = ','.join(new_liat)
            print(str_mobile)

            # 使用celery发送短息
            dict_aa = {}
            dict_aa["contents"] = content
            dict_aa["user_id"] = user_id
            send_sms_code.delay(str_mobile, dict_aa)

            start = start + 4

            # 6.返回结果

        return Response({"massage": "ok"})

class TemplateView(APIView):
    """模板接口"""

    # queryset = Template.objects.all()
    # GenericAPIView, RetrieveModelMixin, UpdateModelMixin
    def get(self, request):
        token = jwt_decode_handler(request.query_params['token'])

        try:
            obj = Template.objects.filter(user=token["user_id"])


        except:
            return Response({"message":"查询出错"})
        if not obj:
            return Response(obj)
        # 线上需要打开
        # user_obj = CustomerInformation.objects.get(id=token["user_id"])
        serializer = GetTemplateSerializer(obj, many=True)

        data = {
            "template":serializer.data,
            # "username":user_obj.username

        }
        return Response(data)

class CreateDeleteTemplateView(RetrieveUpdateDestroyAPIView,ListCreateAPIView):
    """        模板增删改"""

    def post(self, request, *args, **kwargs):
        """保存功能"""

        # 测试数据
        # {
        #     "template_name": "上线版本测试",
        #     "sms_type": "短信",
        #     "user": "老张",
        #     "content": "上线测试早日用户突破100万"
        # }
        data = request.data
        token = jwt_decode_handler(data['token'])
        print(token)

        try:
            obj = Template.objects.filter(template_name=data["template_name"])
        except:
            return Response({"message": "查询出错"})
        if obj:
            return Response({"message": "模板名称已存在"})
        # data_time = time.strftime("%Y-%m-%d")
        # data["data_time"] = data_time
        data["user"] = token["user_id"]
        try:
            user_obj = CustomerInformation.objects.get(id = token["user_id"])
        except:
            return Response({"message":"查询出错"})
        data["username"] = user_obj.first_name
        # 保存操作需要传一个参数
        serializer = TemplateSerializer(data=data)
        # print(serializer.is_valid)
        if serializer.is_valid():
            serializer.save()
            access_token = get_redis_connection('wechatpy').get("access_token").decode()
            Send_template().To_examine_template(token['user_id'], data['content'],access_token)
            return Response({"state": 1})
        else:
            return Response(serializer.errors)

    def delete(self, request, *args, **kwargs):
        """删除操作"""
        data = request.data
        try:
            Template.objects.get(id=data["ID"]).delete()

        except:
            return Response({"message": "删除出错"})

        return Response({"state": 1})

class GetReviewerView(ListAPIView):
    """获取审核模板"""
    queryset = Template.objects.all()
    serializer_class = GetTemplateSerializer

class ReviewerView(CreateAPIView):
    """模板审核"""

    def post(self, request, *args, **kwargs):
        data = request.data
        token = jwt_decode_handler(data['token'])
        try:
            obj = Template.objects.filter(template_name=data["template_name"]).first()

        except:
            return Response({"message":"查询出错"})
        try:
            user_obj = CustomerInformation.objects.get(id = token["user_id"])
        except:
            return Response({"message":"查询出错"})
        data["reviewer_name"] = user_obj.first_name
        serializer = UpdateTemplateSerializer(obj,data,partial=True)
        if serializer.is_valid():
            serializer.save()

        else:
            return Response(serializer.errors)
        access_token = get_redis_connection('wechatpy').get("access_token").decode()

        Send_template().To_examine_template_result(token,obj.state,access_token)
        return Response({"message":"审核成功"})

class SMSView(ListCreateAPIView):
    """首页的发送短信功能"""

    def post(self, request, *args, **kwargs):
        post = request.data
        token = jwt_decode_handler(post['token'])
        # token = post['token']#测试代码
        # 判断企业是否有认证企业
        try:
            user = EnterpriseCertificationInfo.objects.get(user=token.id,identity_status=2)  # 正式代码
            # user = EnterpriseCertificationInfo.objects.get(user=1)
            money_pay = Top_up_Payment.objects.get(userid=user.company_id)

        except:
            return Response({"message": "查询出错"})

        if not user:
            return Response({"message": "认证企业才可以发短信"})
        conn = get_redis_connection("default")
        # 获取存在redis中的数据

        data = conn.get(1)  # 如果redis数据库没有数据
        if data == None:
            return Response({"message": "没有企业可发送"})
        list_obj = pickle.loads(data)
        # 遍历对象
        list_data = []
        for mobile in list_obj:
            # 获取对象对应的手机号
            mobile = mobile.phone
            if mobile:
                #     2.1用正则提取手机号
                # 提取出来的手机
                # 匹配多个手机号
                # "18620885204,18922440038,17603048308,13612238280"
                new_mobile = re.findall(r"1\d{10}", mobile)

                if new_mobile:
                    # 别遍历字符串
                    for number in new_mobile:

                        mobile = re.split(r",", number)
                        for num in mobile:
                            # 放入列表
                            list_data.append(num)
        if post["mobile"]:
            list_data = list_data + post["mobile"]

        print(len(list_data))
        # 判断发送的余额是否充足
        if money_pay.balance < len(list_data) * 0.05:
            data = {
                "message": "余额不足",
                "money": money_pay.balance
            }
            return Response(data)
        """余额加减"""
        # 1.计算总金额
        count_money = money_pay.balance
        print(count_money)
        pay = len(list_data) * 0.05
        print(pay)
        money = float(count_money) - round(pay, 2)
        data = {
            "balance": round(money, 2)
        }

        serializer = MoenyUpdateSerializer(money_pay, data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        n = 0
        while n < len(list_data):
            """以下是判断金额和生成订单号业务逻辑"""

            sms_mobile_list = list_data[n:n + 100]

            obj_first = Template.objects.filter(template_name=post["template_name"], user=token.username).first()
            # print(obj_first)
            str_mobile = ','.join(sms_mobile_list)

            """以下生成订单"""
            # 随机生成订单号
            num_six = random.randint(1, 1000000)
            order_id = datetime.now().strftime("%Y%m%d%H%M%S") + "1" + "%08d" % num_six

            # 单批总金额计算
            money_count = len(sms_mobile_list) * 0.05
            order_data = {
                "order_id": order_id,  # 订单id
                "company_id": user.company_id,  # 认证企业id
                "total_count": len(sms_mobile_list),  # 号码总数
                "total_amount": round(money_count, 2),  # 单批总金额
                "sms_type": "短信",  # 发送类型
                "username": "老王",  # 用户名
                "mobile": str_mobile,  # 手机号
                "price": 0.05  # 单价
            }
            # 保存订单操作
            serializer = SaveOrderSerializer(data=order_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)

            n += 100




            # dict_aa = {}
            # dict_aa["contents"] = obj_first.content
            # dict_aa["username"] = post["name"]
            # # print(dict_aa)
            # # 以下是发送短信代码上线或测试时候需要打开
            # # send_sms_code.delay(str_mobile, dict_aa)
            # # 保存数据库信息
            # obj_data = {}
            # # # 1.行业
            # obj_data["industry"] = post["industry"]
            # # # # 2.省份
            # obj_data["province"] = post["province"]
            # # # # 3.经营范围
            # obj_data["business_scope"] = post["business_scope"]
            # # # # 4.过滤已送号码
            # obj_data["filter"] = str_mobile
            # # # # 5.发送内容
            # obj_data["content"] = post["content"]
            # # # # 6.每批的id
            # order_no = str(time.strftime('%Y%m%d', time.localtime(time.time()))) + str(time.time()).replace('.', '')[
            #                                                                        -7:]
            # # obj_data["task_id"] = order_no
            # # serializer = ManualMessagePostSerializer(data=obj_data, partial=True)
            # # if serializer.is_valid():
            # #     serializer.save()
            #
            #
            # # else:
            # #     return Response(serializer.errors)

        return Response({"code": 1})













        # class SMSView(ListCreateAPIView):
        #     """首页的发送短信功能"""
        #
        #     def post(self, request, *args, **kwargs):
        #         post = request.data
        #         conn = get_redis_connection("default")
        #         data = conn.get(post["token"].id)
        #
        #         # 如果数据库没有数据
        #         if data == None:
        #             pass
        #         list_obj = pickle.loads(data)
        #         # 遍历对象
        #         list_data = []
        #         for mobile in list_obj:
        #             # 获取对象对应的手机号
        #             mobile = mobile.phone
        #             if mobile:
        #                 #     2.1用正则提取手机号
        #                 # 提取出来的手机
        #                 # 匹配多个手机号
        #                 # "18620885204,18922440038,17603048308,13612238280"
        #                 new_mobile = re.findall(r"1\d{10}", mobile)
        #
        #                 if new_mobile:
        #                     # 别遍历字符串
        #                     for number in new_mobile:
        #
        #                         mobile = re.split(r",", number)
        #                         for num in mobile:
        #                             # 放入列表
        #                             list_data.append(num)
        #
        #         n = 0
        #
        #         print(list_data)
        #         while n < len(list_data):
        #
        #             sms_mobile_list = list_data[n:n + 100]
        #
        #             obj_first = Template.objects.filter(template_name=post["template_name"], user=post["name"]).first()
        #             # print(obj_first)
        #             str_mobile = ','.join(sms_mobile_list)
        #
        #             dict_aa = {}
        #             dict_aa["contents"] = obj_first.content
        #             dict_aa["username"] = post["name"]
        #             # print(dict_aa)
        #             # 以下是发送短信代码上线或测试时候需要打开
        #             # send_sms_code.delay(str_mobile, dict_aa)
        #             obj_data = {}
        #             # # 1.行业
        #             obj_data["industry"] = post["industry"]
        #             # # # 2.省份
        #             obj_data["province"] = post["province"]
        #             # # # 3.经营范围
        #             obj_data["business_scope"] = post["business_scope"]
        #             # # # 4.过滤已送号码
        #             obj_data["filter"] = str_mobile
        #             # # # 5.发送内容
        #             obj_data["content"] = post["content"]
        #             # # # 6.每批的id
        #             order_no = str(time.strftime('%Y%m%d', time.localtime(time.time()))) + str(time.time()).replace('.', '')[
        #                                                                                    -7:]
        #             obj_data["task_id"] = order_no
        #             serializer = ManualMessagePostSerializer(data=obj_data, partial=True)
        #             if serializer.is_valid():
        #                 serializer.save()
        #
        #             else:
        #                 return Response(serializer.errors)
        #
        #             n += 100
        #
        #         return Response({"code": 1})














        # # 获取客户端填写的内容
        # data = request.data
        # print(data)
        # # 链接redis
        # conn = get_redis_connection("sms_code")
        #
        # mobile = '13612238280'
        # conn.set("sms_code", mobile)
        #
        # # 生成管道对象
        # pl = conn.pipeline(mobile)
        # pl.execute()
        #
        # # 获取存在redis中的手机号
        # mobile = conn.get("sms_code").decode()
        # print(mobile)
        # contents = data["contents"]
        # # 使用celery发送短息
        # username = 'laowang'
        # dict_aa = {}
        # dict_aa["contents"] = contents
        # dict_aa["username"] = username
        # send_sms_code.delay(mobile, dict_aa)
        #
        # # 5、返回结果
        # return Response({'message': 'ok'})

class AccurateView(APIView):
    """精准短信信息"""
    def get(self,request):

        provinces = request.GET['provinces']

        industryid = request.GET['industryid']

        business = request.GET['business']

        if business:
            try:
                # 查询行业对应的省份的所有企业返回F
                # # 参数对应的行业
                i = value(int(industryid))

                # # orm查询总数
                all_obj = globals()[i].objects.filter(province__startswith=provinces,business_scope__contains=business)



            except:
                return Response({"code": 2})
                # 如果查询为空字符集
            if all_obj.exists() == False:
                return Response({"code": 1})

            data_list = []
            # 遍历obj对象
            all_data_list =[]
            for obj in all_obj:
                all_data_dict = {}
                mobile = obj.phone


                all_data_dict["enterprises"] = obj.company_name
                all_data_dict["kind"] = obj.kind

                if mobile:
                    #     2.1用正则提取手机号
                    all_data_dict["mobile"] = mobile[:7] + "****"
                    # 提取出来的手机
                    # 匹配多个手机号
                    # "18620885204,18922440038,17603048308,13612238280"
                    new_mobile = re.findall(r"1\d{10}", mobile)
                    data_dict = {}
                    if new_mobile:
                        # 别遍历字符
                        data_dict["mobile"] = new_mobile[0][:7] + "****"
                        data_dict["enterprises"] = obj.company_name
                        data_dict["kind"] = obj.kind
                        data_list.append(data_dict)
                all_data_list.append(all_data_dict)
            if len(data_list) < 16 or len(all_data_list) < 16:
                data = {
                    "count": len(data_list),
                    "info": data_list,
                    "all_count": all_obj.count(),
                    "all_info": all_data_list
                }
                return Response(data)


            # 随机16个筛选后的数据
            sample = random.sample(xrange(len(data_list)), 16)
            result = [data_list[i] for i in sample]
            # 随机16个没有筛选的数据
            s = random.sample(xrange(len(all_data_list)), 16)
            r = [all_data_list[i] for i in s]

            data = {
                "count": len(data_list),
                "info": result,
                "all_count":all_obj.count(),
                "all_info":r
            }

            return Response(data)




        try:
            # 查询行业对应的省份的所有企业返回F
            # # 参数对应的行业
            i = value(int(industryid))
            # # orm查询总数
            all_obj = globals()[i].objects.filter(province__startswith=provinces).filter()

        except:
            return Response({"code": 2})
            # 如果查询为空字符集
        if all_obj.exists() == False:
            return Response({"code": 1})
        data_list = []
        #遍历obj对象
        all_data_list = []
        for obj in all_obj:

            all_data_dict = {}
            mobile = obj.phone


            all_data_dict["enterprises"] = obj.company_name
            all_data_dict["kind"] = obj.kind


            if mobile:
                all_data_dict["mobile"] = mobile[:7] + "****"
                #     2.1用正则提取手机号
                # 提取出来的手机
                # 匹配多个手机号
                # "18620885204,18922440038,17603048308,13612238280"
                new_mobile = re.findall(r"1\d{10}", mobile)
                data_dict = {}
                if new_mobile:
                    # 别遍历字符
                    data_dict["mobile"] = new_mobile[0][:7] + "****"
                    data_dict["enterprises"] = obj.company_name
                    data_dict["kind"] = obj.kind
                    data_list.append(data_dict)
            all_data_list.append(all_data_dict)

        if len(data_list) < 16 or len(all_data_list) <16:
            data = {
                "count": len(data_list),
                "info": data_list,
                "all_count": all_obj.count(),
                "all_info": all_data_list
            }

            return Response(data)
        #随机16个筛选后的数据
        sample = random.sample(xrange(len(data_list)), 16)
        result = [data_list[i] for i in sample]
        #随机16个没有筛选的数据
        s = random.sample(xrange(len(all_data_list)), 16)
        r = [all_data_list[i] for i in s]


        data = {
            "count":len(data_list),
            "info":result,
            "all_count": all_obj.count(),
            "all_info": r

        }

        return Response(data)

class BalanceInfoView(APIView):
    """余额查询"""
    def get(self,request):

        provinces = request.GET['provinces']
        industryid = request.GET['industryid']
        business = request.GET['bussiness']
        phone = request.GET["mobile"]
        token = jwt_decode_handler(request.query_params['token'])
        print(token)
        try:
            obj = EnterpriseCertificationInfo.objects.filter(user=token["user_id"],identity_status=2)
            pay_obj = Top_up_Payment.objects.filter(userid=obj[0].company_id)
            print(pay_obj)
            print(obj)
        except:
            return Response({"message":"查询出错"})
        if not obj:
            return Response({"message":"没有认证企业"})

        if business:
            try:
                # 查询行业对应的省份的所有企业返回F
                # # 参数对应的行业
                i = value(int(industryid))

                # # orm查询总数
                all_obj = globals()[i].objects.filter(province__startswith=provinces,business_scope__contains=business)

            except:
                return Response({"code": 2})

            list_data = []

            for mobile in all_obj:
                # 获取对象对应的手机号
                mobile = mobile.phone
                if mobile:
                    #     2.1用正则提取手机号
                    # 提取出来的手机
                    # 匹配多个手机号
                    # "18620885204,18922440038,17603048308,13612238280"
                    new_mobile = re.findall(r"1\d{10}", mobile)

                    if new_mobile:
                        # 别遍历字符串
                        for number in new_mobile:

                            mobile = re.split(r",", number)
                            for num in mobile:

                                # 放入列表
                                list_data.append(num)
            if phone:
                list_data = list_data + phone
            count_money = len(list_data) * 0.05  # 电话号码数乘单价
            money = obj[0].balance  # 用户余额
            # consumption_money = money - count_money
            data = {
                "count_money": round(count_money,2),
                "money": money,
                "mobile_count": len(list_data),
                "company_name": obj[0].name
            }
            return Response(data)

        try:
            # 查询行业对应的省份的所有企业返回F
            # # 参数对应的行业
            i = value(int(industryid))
            # # orm查询总数
            all_obj = globals()[i].objects.filter(province__startswith=provinces).filter()

        except:
            return Response({"code": 2})

        list_data = []

        for mobile in all_obj:
            # 获取对象对应的手机号
            mobile = mobile.phone
            if mobile:
                #     2.1用正则提取手机号
                # 提取出来的手机
                # 匹配多个手机号
                # "18620885204,18922440038,17603048308,13612238280"
                new_mobile = re.findall(r"1\d{10}", mobile)

                if new_mobile:
                    # 别遍历字符串
                    for number in new_mobile:

                        mobile = re.split(r",", number)
                        for num in mobile:
                            # 放入列表
                            list_data.append(num)
        if phone:
            list_data = list_data + phone
        count_money = len(list_data)*0.05 #电话号码数乘单价
        money = pay_obj[0].balance  #用户余额
        # consumption_money = money-count_money# 消费后还剩多少钱
        data = {
            "count_money": round(count_money,2),
            "money": money,
            "mobile_count": len(list_data),
            "company_name": obj[0].name
        }
        return Response(data)

class AuthenticationAuditTemplateView():
    """认证审核模板"""
    def post(self, request, *args, **kwargs):
        data = request.data
        token = jwt_decode_handler(data['token'])
        print(token)
        try:
            obj = EnterpriseCertificationInfo.objects.filter(company_id=data["company_id"]).first()

        except:
            return Response({"message":"查询出错"})
        try:
            user_obj = CustomerInformation.objects.get(id = token["user_id"])
        except:
            return Response({"message":"查询出错"})
        data["reviewer_name"] = user_obj.first_name
        serializer = AuthenticationAuditTemplateSerializer(obj,data,partial=True)
        if serializer.is_valid():
            serializer.save()

        else:
            return Response(serializer.errors)
        return Response({"message":"审核成功"})

class PayCertificationView(ListCreateAPIView):
    """认证支付"""
    def post(self, request, *args, **kwargs):
        data = request.data
        token = jwt_decode_handler(request.data['token'])
        num_six = random.randint(1, 1000000)
        order_id = datetime.now().strftime("%Y%m%d%H%M%S") + "1" + "%08d" % num_six
        user_id =token["user_id"]
        openid = token["username"]

        pay_info = get_pay_info(openid, user_id, order_id, "1")

        data={
            "order_id":order_id,
            "user_id":user_id,
            "openid":openid,
            "mobile":data["mobile"],
            "name":data["name"],
            "money":200.00
        }

        serializer = PayCertificationSerializer(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"pay_info":pay_info})
        else:
            return Response(serializer.errors)



