import re
from urllib import parse

import pickle
import random

# Create your views here.
from django.http import HttpResponse
from django_redis import get_redis_connection

from drf_haystack.viewsets import HaystackViewSet
from jieba import xrange
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin

from rest_framework.response import Response
from rest_framework.utils import json

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from Enterprise.models import *
from Enterprise.utils import EnterprisesPageNum, value, num_func, EnterprisePageNum
# from Users.models import User
from Industry.models import *
from Monitor.utils import monitor
from Subseribe.models import Bids
from Subseribe.views import BidsSearchView
from Users.models import EnterpriseCertificationInfo
from oauth.models import CustomerInformation
from  rest_framework_jwt.utils import jwt_decode_handler
from .serializables import RecommendedSerializer, ListSerializer, DefaultSerializer, \
    MatchingInfoSerializer, SingleSerializer, SingleUpSerializer, \
    AreaSerializer, AndustrySerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage

class IndexView(APIView):
    """首页企业信息"""
    # 用户需要经过认证的
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token = jwt_decode_handler(request.query_params['token'])

        except Exception as e:
            return Response({"token_state": False})
        monitor(token, "index/info")


        try:

            data = EnterpriseCertificationInfo.objects.filter(user=token["user_id"],identity_status=2).first()
        except:
            return Response({"massage":False})
        if data:
            data_info = {
                    "enterprise": data.name,  # 企业名字
                    "enterpriseid": data.company_id,  # 企业id
                    "code": 0,  # 成功
                    "industryid": data.industryid,  # 行业
                    # 临时数据推荐数量和访问数量
                    "identity_status": True,
                    "count": data.access,  # 访问数总量
                    "number": data.recommended,  # 推荐数
                    "matching":0
                }
            return Response(data_info)

        #if data.exists() == False:
            # 随机
        num = random.randint(1, 19)

        i = value(num)
            # print(i)
        list_data = globals()[i].objects.filter()
        sample = random.sample(xrange(list_data.count()), 1)

        result = [list_data[i] for i in sample]
            # 字符串类查询
        #j = num_func(num)
        #str_num = str(result[0].company_id)
            # # obj_data = globals()[j].objects.filter(company_id=result[0].company_id).first()
        #obj_data = globals()[j].objects.get(company_id=str_num)
        #obj_data.access_count += 1
        #obj_data.save()

            # 分割出所有
        kind = result[0].kind

        if  kind:

                #print(kind)
            matching = kind.split("|")
                #print(matching)
            dids_list = []
            for i in matching:
                bids = Bids.objects.filter(Title__contains=i)
                for p in bids:
                    dids_list.append(p)
		
            data_dict = {
                    "enterprise": result[0].company_name,  # 企业名字
                    "enterpriseid": result[0].company_id,  # 行业id
                    "code": 0,  # 成功
                    "industryid": num,  # 行业
                    # 临时数据推荐数量和访问数量
                    "identity_status": False,
                    #"count": obj_data.access_count,  # 访问数总量
                    #"number": obj_data.recommended_count,  # 推荐数
                    "count":0,
                    "number":0,
                    "matching":len(dids_list)
                }
            return Response(data_dict)
        data_dict = {
                "enterprise": result[0].company_name,  # 企业名字
                "enterpriseid": result[0].company_id,  # 行业id
                "code": 0,  # 成功
                "industryid": num,  # 行业
                # 临时数据推荐数量和访问数量
                "identity_status": False,
                #"count": obj_data.access_count,  # 访问数总量
                #"number": obj_data.recommended_count,  # 推荐数
                "count":0,
                "number":0,
                "matching":0

            }
        return Response(data_dict)
     
           

class IndexIndustryView(APIView):
    """下链省份数据返回"""

    def get(self, request):
        # 获取行业对应的id
        # print(industryid)


        try:
            list_data = Chain.objects.all()
            # list_data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

            sample = random.sample(xrange(list_data.count()), 6)

            result = [list_data[i] for i in sample]



        except:
            return Response({'message': "查询错误"})

        zong_list = []

        # industry_list = []

        try:
            # 格式:[{行业:{name:,id:}},省份数据:[{广东:100}]]
            # 行业名字
            for j in result:

                #   查询6个行业对应的的数据
                # print(j.industry)
                dict_industry = {}
                # 行业字典
                dict_industry["Name"] = j.industry
                dict_industry["ID"] = j.id
                # industry_list.append(dict_industry)
                # print("+++++++")
                # count_data = Count.objects.filter(industry=j.id).filter()
                # 查询数量条件要改：比如说：查询的时候行业对应的
                count_data = Datasummary.objects.filter(industry=j.eng_industry).filter()

                # print(count_data)
                # print(count_data)

                provinces_list = []

                # 省份字典
                for i in count_data:
                    # print(i.province)
                    dict_provinces = {}

                    provinces = Provinces.objects.filter(provinces=i.province)
                    # print(provinces[0].id)
                    # print(provinces)
                    dict_provinces["Name"] = i.province
                    dict_provinces["Count"] = i.amount
                    dict_provinces["ID"] = provinces[0].id

                    provinces_list.append(dict_provinces)

                zong_dict = {}
                zong_dict["ClassName"] = dict_industry
                zong_dict["Province"] = provinces_list

                zong_list.append(zong_dict)



        except:
            return Response({"code": 0})

        return Response(zong_list, status=200)

class UpIndexIndustryView(APIView):
    """上链数据返回"""

    # 上链业务逻辑  大类总共有十四个
    # 1.随机六个数据大类的所有省份数据
    #
    # 2.查询六个大类数据
    def get(self, request):

        try:
            up_chain_obj = DatasummaryForUp.objects.all()
            # print(up_chain_obj)
            # print(up_chain_obj[0])
            up_chain_list = []
            for up_obj in up_chain_obj:
                up_chain_list.append(up_obj.industry)

            # 去从
            new_list = list(set(up_chain_list))
            # 随机6
            samples = random.sample(xrange(len(new_list)), 6)
            results = [new_list[i] for i in samples]

            zong_list = []

            for up_chain in results:
                up_obj_data = {}
                up_obj_data["Name"] = up_chain
                p_data = DatasummaryForUp.objects.filter(industry=up_chain).filter()

                count_list = []
                for new_p_data in p_data:
                    up_province_data = {}
                    up_province_data["Name"] = new_p_data.province
                    up_province_data["Count"] = new_p_data.amount
                    up_obj_data["ID"] = new_p_data.industryid

                    # print(up_province_data)
                    count_list.append(up_province_data)

                zong_dict = {}
                zong_dict["ClassName"] = up_obj_data
                zong_dict["Province"] = count_list
                zong_list.append(zong_dict)
                # print(zong_list)
        except:
            return Response({"message": "查询出错"})

        return Response(zong_list)

class RecommendedView(GenericAPIView):
    """我推荐"""

    def post(self, request):

        # 我推荐重写，推荐企业加1自己也加1，还要有记录

        # 1.获取传回来的指定功能参数
        try:
            data = request.data
        #print(data)
            token = jwt_decode_handler(data['token'])
        except:
            return Response({"token_state":False})
        # 2.如果拿获取到的数据对应修改
        try:
            obj = EnterpriseCertificationInfo.objects.filter(user = token["user_id"],identity_status=2).first()
        except:
            return Response({"message":"查询出错"})
        if obj:
            obj.recommended +=1
            obj.save()
        try:
            # 查询对应的企业和用户的信息
            state = Function.objects.filter(user_id=obj.company_id, company_id=data["company_id"])

            if data["i_recommend"] == True and state.exists() == False:

                j = num_func(data["industryid"])
                obj_data = globals()[j].objects.get(company_id=data["company_id"])
                obj_data.recommended_count += 1
                obj_data.save()
                # 保存状态操作
                serializer = RecommendedSerializer(data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response({"state": 1})
                else:
                    return Response(serializer.errors)

            if state[0].i_recommend:
                return Response({'message': '你已经推荐过该企业'})
                # 更新操作
            serializer = RecommendedSerializer(state, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"state": 1})
            else:
                return Response(serializer.errors)

        except:
            return Response({"message": "程序出错"})

class BasicInformationView(APIView):
    """企业基本信息实现"""

    def get(self, request):

        # 1.需要的参数【行业id，企业id】
        enterpriseid = request.GET["enterpriseid"]
        # print(enterpriseid)
        industryid = request.GET["industryid"]
        # print(industryid)
        if not industryid:
            return Response({"message": "该企业没有信息"})
        try:
            i = value(int(industryid))
            list_data = globals()[i].objects.filter(company_id=enterpriseid).values()
            # print(list_data)
        except:
            return Response({"code": 1})

        data = {
            "basic": list_data,
            "code": 0
        }
        return Response(data)

class ListView(APIView):
    """实现列表数据返回功能"""
    # permission_classes = [IsAuthenticated]
    # 1.获取维度的信息查询维度的所有信息并只返回企业信息7家和所有企业数量
    def get(self, request):
        # 获取用户点击的维度名称
        # 1.下链需要获取的参数
        conn = get_redis_connection("default")
        logo = request.GET["logo"]
        provinces = request.GET['provinces']
        industryid = request.GET['industryid']
        # name = request.GET['name']
        try:
            token = jwt_decode_handler(request.query_params['token'])

        except Exception as e:
            return Response({"token_state": False})
        name = token["username"]
        if logo == "down":

            try:
                # 查询行业对应的省份的所有企业返回F
                # # 参数对应的行业
                i = value(int(industryid))
                # # orm查询总数
                all_data = globals()[i].objects.filter(province__startswith=provinces).filter()

            except:
                return Response({"code": 1})
            # 如果查询为空字符集
            if all_data.exists() == False:
                return Response({"code": 1})

            list_data = []
            for j in all_data:
                dict_data = {}
                if j.phone:
                    dict_data["mobile"] = j.phone[:7] + "****"

                dict_data["enterprises"] = j.company_name
                dict_data["enterprisesid"] = j.company_id
                dict_data["kind"] = j.kind

                list_data.append(dict_data)

            # # print(all_data.count())
            # if all_data.count() < 16:
            #     conn.set(name, pickle.dumps(all_data), 1024 * 500)
            #     data = {
            #         "count": all_data.count(),
            #         "enterprises_data": list_data,
            #         .
            #
            #     }
            #     return Response(data)

            conn.set(name, pickle.dumps(all_data),1024 * 500)
            # conn.expire('name', 1024 * 500)
            sample = random.sample(xrange(all_data.count()), 16)
            result = [list_data[i] for i in sample]
            data = {
                "count": all_data.count(),
                "enterprises_data": result,
                "code": 0
            }
            # serializer = ListSerializer(all_data, many=True)
            # print(list(serializer.data))
            # 处理数据庞大返回个数
            # sample = random.sample(xrange(all_data.count()), 10)
            # result = [serializer.data[i] for i in sample]
            return Response(data)

        up_industry = request.GET['up_industry']

        try:
            # 查询行业对应的省份的所有企业返回
            # # 参数对应的行业
            i = value(int(industryid))
            # print(i)
            # # orm查询总数
            all_data = globals()[i].objects.filter(province__startswith=provinces,
                                                   industry_involved=up_industry).filter()
            # print(all_data)

        except:
            return Response({"code": 1})
        # 如果查询为空字符集
        if all_data.exists() == False:
            return Response({"code": 1})

        list_data = []
        for j in all_data:
            dict_data = {}
            if j.phone:
                dict_data["mobile"] = j.phone[:7] + "****"

            dict_data["enterprises"] = j.company_name
            dict_data["enterprisesid"] = j.company_id
            dict_data["kind"] = j.kind
            list_data.append(dict_data)

        # print(all_data.count())
        # if all_data.count() < 16:
        #     conn.delete("enterprises_data")
        #     data = {
        #         "count": all_data.count(),
        #         "enterprises_data": list_data,
        #         "code": 2
        #
        #     }
        #     return Response(data)

        conn.set(name, pickle.dumps(all_data),1024 * 500)
        # conn.expire('name', 1024 * 500)
        sample = random.sample(xrange(all_data.count()), 16)
        result = [list_data[i] for i in sample]

        data = {
            "count": all_data.count(),
            "enterprises_data": result,
            "code": 0
        }
        # serializer = ListSerializer(all_data, many=True)
        # print(list(serializer.data))
        # 处理数据庞大返回个数
        # sample = random.sample(xrange(all_data.count()), 10)
        # result = [serializer.data[i] for i in sample]
        return Response(data)

class InBatchView(APIView):
    """换一批"""

    def get(self, request):
        # 连接redis数据库
        try:
            token = jwt_decode_handler(request.query_params['token'])

        except Exception as e:
            return Response({"token_state": False})
        conn = get_redis_connection("default")
        # 获取存在redis的数据
        data = conn.get(token["username"])
        list_obj = pickle.loads(data)


        if list_obj.count() < 16:
            data = {
                "code":2 # 代表没有超过16个数据可以换一批
            }
            return Response(data)

        list_data = []
        for j in list_obj:
            dict_data = {}
            if j.phone:
                dict_data["mobile"] = j.phone[:7] + "****"
            dict_data["enterprises"] = j.company_name
            dict_data["enterprisesid"] = j.company_id
            dict_data["kind"] = j.kind

            list_data.append(dict_data)

        sample = random.sample(xrange(list_obj.count()), 16)
        result = [list_data[i] for i in sample]

        data = {
            "enterprises_data": result,
            "code": 0
        }
        # 返回结果

        return Response(data)

class ColumnView(APIView):
    """首页随机认证滚动条"""

    def get(self, request):
        num = random.randint(1, 19)
        i = value(num)
        # print(i)
        list_data = globals()[i].objects.filter()
        sample = random.sample(xrange(list_data.count()), 1)
        result = [list_data[i] for i in sample]
        enterprise = result[0].company_name

        data = {
            "enterprise": enterprise
        }

        return Response(data)

class SearchFunctionView(APIView):
    """访问和推荐数"""

    def get(self, request):
        company_id = request.GET["company_id"]
        try:
            obj = EnterpriseCertificationInfo.objects.filter(company_id=company_id).first()

        except:
            return Response({"message": "查询出错"})
        if obj:
            num = request.GET["industrysid"]
            j = num_func(int(num))
            try:

                obj_data = globals()[j].objects.get(company_id=str(company_id))
            except:
                return Response({"message": "查询出错"})

            data = {
                "access_count": obj_data.access_count,
                "recommended_count": obj_data.recommended_count,
                "authentication": True
            }

            return Response(data)

        num = request.GET["industrysid"]
        j = num_func(int(num))
        try:

            obj_data = globals()[j].objects.get(company_id=str(company_id))
        except:
            return Response({"message": "查询出错"})

        data = {
            "access_count": obj_data.access_count,
            "recommended_count": obj_data.recommended_count,
            "authentication": False
        }

        return Response(data)

class SingleIndustryView(APIView):
    """单一查询行业省份数据"""

    def get(self,request):
        logo = request.GET["logo"]
        if logo=="down":
            pk = request.GET["id"]
            try:
                data = Datasummary.objects.filter(industry=Chain.objects.filter(id=pk).first().eng_industry).filter()
            except:
                return Response({"message":"查询出错"})

            serializer = SingleSerializer(data,many=True)

            return Response(serializer.data)

        industry_involved = request.GET["industry_involved"]

        try:
            data = DatasummaryForUp.objects.filter(industry=industry_involved).filter()

        except:
            return Response({"message":"查询错误"})

        serializer = SingleUpSerializer(data, many=True)

        return Response(serializer.data)

class AreasViews(ListAPIView):
    """
    地区信息
    """
    serializer_class = AreaSerializer
    queryset = Provinces.objects.all()

    # @cache_response(timeout=60 * 60, cache='default')
    #def get(self, request, *args, **kwargs):
    #    return self.list(self, request, *args, **kwargs)

class EnterpriseMarketingView(ListAPIView):
    """
    行业信息
    """
    serializer_class = AndustrySerializer
    queryset = Chain.objects.all()

    # @cache_response(timeout=60 * 60, cache='default')
    # def get(self, request, *args, **kwargs):
    #     return self.list(self, request, *args, **kwargs)

class MarketingConfigurationView(APIView):
    """
    营销配置创建
    """
    # serializer_class = MarketingprovincesSerializer
    # queryset = OauthQYUser.objects.all()
    def post(self, request, *args, **kwargs):
        """
        营销配置创建
        """
        # 获取数据字典
        data_dict = request.data

        # 数据处理
        areas = data_dict['areas'].split(",")
        marketing = data_dict['marketing'].split(",")
        enterprise_id = data_dict['enterprise_id']

        try:
            mrke = EnterpriseCertificationInfo.objects.get(id=enterprise_id)
        except Exception:
            return Response({
                "message": "已设置,请点击修改.无法再次保存!"
            })

        # 正向添加
        mrke.weidu.add(*marketing)
        mrke.areas.add(*areas)

        return Response({
            "message":'保存成功'
        })

    def put(self,request):
        # 获取前端数据
        data_dict = request.data
        # user = User.objects.get(id=1)
        user =request.user
        # 如果同时传递了instance,data表示需要更新数据

        # 企业对象
        enterprise = user.enterprise
        marketing = data_dict['marketing'].split(",")
        areas = data_dict['areas'].split(",")

        # 正向修改
        enterprise.weidu.set(*marketing)
        enterprise.areas.set(*areas)

        return Response({
            "message": '保存成功'
        })

    def get(self,request):
        """
        获取营销配套信息
        :param request:
        :return:
        """
        user = CustomerInformation.objects.get(id=1)
        # user = request.user
        # 企业对象
        enterprise = user.enterprise
        if enterprise is None:
            return Response({
                "message": '未认证',
            })
        weidu_list =[]
        for weidu in enterprise.weidu.all():
            weidu_list.append(weidu.industry)
        area_list = []
        for area in enterprise.areas.all():
            area_list.append(area.provinces)
        return Response({
            "message": '查询成功',
            'industry':weidu_list,
            'areas':area_list
        })

class MatchingDemandView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin):

    serializer_class = MatchingInfoSerializer
    queryset = EnterpriseCertificationInfo.objects.all()

    def get(self, request, *args, **kwargs):
        """获取配套需求"""
        return self.retrieve(request, *args, **kwargs)

    @action(methods=["put"], detail=True)
    def update(self, request, *args, **kwargs):
        """配套需求修改"""
        # 获取配套需求, 获取数据
        demand = self.get_object()
        dict_data = request.data


        # 使用序列化器实现
        serializer = MatchingInfoSerializer(instance=demand, data=dict_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 返回响应
        return Response(serializer.data)

