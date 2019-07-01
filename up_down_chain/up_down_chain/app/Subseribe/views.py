import re
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from  rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.response import Response
from rest_framework.views import APIView
from Enterprise.models import Provinces
from Enterprise.serializables import AreaSerializer
from Users.models import EnterpriseCertificationInfo
from up_down_chain.utils.endtoday import rest_of_day
from Industry.utils import EnterprisePageNum
from oauth.models import CustomerInformation
from up_down_chain.utils.send_template import Send_template
from .serializers import  KeywordSerializer, BidsIndexSerializer, RetrieveIndexSerializer
from .models import Bids, BidsUserSetting
from django_redis import get_redis_connection
import datetime



class RemindInfoViews(GenericAPIView):
    """
    关键词设置
    """
    serializer_class = KeywordSerializer

    def get(self,request):
        dict_data= request.query_params
        try:
            token = jwt_decode_handler(dict_data['token'])
            user = CustomerInformation.objects.get(id=token['user_id'])
        except Exception as e:
            return Response({"token_state":False})
        try:
            bid = BidsUserSetting.objects.get(mid=user.id)
        except Exception:
            return Response({
                "message": False,
            })

        bid_serializer =self.get_serializer(bid)
        data_dict = bid_serializer.data
        area_list =data_dict['areas_id'].split(",")
        area = Provinces.objects.filter(id__in=area_list)
        areaserialzer = AreaSerializer(instance=area,many=True)
        return Response({
            'area':areaserialzer.data,
            'data_dict':data_dict,
            "message": True,
        })

    def post(self,request):
        """
        关键词设置
        """
        # request.data['user_id']
        # 获取前端数据
        dict_data = request.data
        try:
            token = jwt_decode_handler(dict_data['token'])
            user = CustomerInformation.objects.get(id=token['user_id'])
        except Exception as e:
            return Response({"token_state":False})
        # 判断关键字是否包含特殊字符
        keywords_array = dict_data['keywords_array']


        for keyword in keywords_array.split(","):
            if bool(re.search('\W+', keyword)) or 2 > len(keyword) >= 7:
                return Response({"message": "关键词不能包含特殊字符或者超过2-6个字,请修改后保存"}, status=status.HTTP_404_NOT_FOUND)
        area_name = dict_data['area_name']

        try:
            bid = BidsUserSetting.objects.get(mid_id=user.id)
            serializer = self.get_serializer(instance=bid, data=dict_data)
        except Exception:
            dict_data['mid'] = user.id
            # 没有该对象则创建
            serializer = self.get_serializer(data=dict_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        access_token = get_redis_connection('wechatpy').get("access_token").decode()
        Send_template().To_Examine_Template_Subscribe(user,serializer.data['keywords_array'],area_name,access_token)


        return Response({
            'data_dict':serializer.data,
            "message": "保存成功",
        })

    # def put(self,request):
    #     # 获取前端数据
    #     dict_data = request.data
    #
    #     token = jwt_decode_handler(dict_data['token'])
    #
    #     user = CustomerInformation.objects.get(id=token['user_id'])
    #     # 判断关键字是否包含特殊字符
    #     try:
    #         keywords_array = dict_data['keywords_array']
    #     except Exception:
    #         return Response({
    #             "message": "关键字不许为空",
    #         })
    #
    #     for keyword in keywords_array.split(","):
    #         if bool(re.search('\W+', keyword)) or 2 > len(keyword) >= 7:
    #             return Response({"message": "关键词不能包含特殊字符或者超过2-6个字,请修改后保存"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     del dict_data['token']
    #     dict_data['mid'] = user.id
    #     try:
    #         bid = BidsUserSetting.objects.get(mid_id=user.id)
    #         serializer = self.get_serializer(instance=bid, data=dict_data)
    #     except Exception:
    #         # 没有该对象则创建
    #         serializer = self.get_serializer(data=dict_data)
    #
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({
    #         'data_dict': serializer.data,
    #         "message": "保存成功",
    #     })
        # try:
        #     user = request.user
        # except Exception as e:
        #     user = None
        # if user and request.user.is_authenticated:
        #
        # return Response({
        #     "message": "用户不存在",
        # })

# class BidsSearchViewSet(APIView):
#     """
#     推送筛选
#     """
#     # permission_classes = [IsAuthenticated]
#     def get(self,request):
#         # token = jwt_decode_handler(request.query_params['token'])
#
#         data_ditc = request.query_params
#         user = CustomerInformation.objects.get(id=data_ditc['user_id'])
#         try:
#             bid = BidsUserSetting.objects.get(mid=user.id)
#         except Exception:
#             return Response({
#                 "message": False,
#             })
#         else:
#
#             # 　文章id列表
#             id_dict = set()
#             # 时间字典
#
#             data_dict_time = set()
#
#             # 数据类型转换
#             end_num = int(data_ditc.get('end_num'))
#             areas = data_ditc.get('areas')
#             keywords = data_ditc.get('keywords')
#             begin_num = end_num - 10
#
#
#             # 判断是否为空,若是空则去数据库查找
#             if keywords is None and areas is None:
#                 keywords = bid.keywords_array
#                 areas = bid.areas
#
#
#             from django.db.models import Q  # 框架原因手动导入Q
#             if areas == '0':
#                 try:
#                     # 　过滤查询
#                     articles = Bids.objects.filter(Title__in=keywords.split(","))
#                     # articles = Bids.objects.all()
#                 except Exception:
#                     return Response({"message": "查询出错"})
#
#             else:
#                 # 把地区编号转为列表
#                 list_area = areas.split(",")
#
#
#                 try:
#                     #Q(content__in=keywords.split(",")) |
#                     # 　过滤查询
#                     articles = Bids.objects.filter(Title__in=keywords.split(","),CreateTime__lte=user.CreateTime, BidsAreaID_id__in=list_area).exclude(id__in=id_dict)[begin_num:end_num]
#                 except Exception:
#                     return Response({"message": "查询出错"})
#                 if articles.exists():  # 判断是否存在queryset
#                     serializer = FastSeekSerializer(articles, many=True)
#                     for article in serializer.data:
#                         id_dict.add(article['id'])  # 防止重复数据
#                         data_dict_time.add(article['CreateTime'])
#
#                     data_ditc_content = {}
#                     for time in data_dict_time:
#                         list_a = []
#                         for article in serializer.data:
#                             if time == article['CreateTime']:
#                                 list_a.append(article)
#                                 data_ditc_content[time] = list_a
#
#                 return Response({"message": "没有内容"})

class Casual_Go(HaystackViewSet):
    """随便逛逛"""

    index_models = [Bids]
    serializer_class = BidsIndexSerializer
    pagination_class = EnterprisePageNum

    def retrieve(self, request, *args, **kwargs):
        return False

class BidsSearchViewSet(HaystackViewSet):
    """实现搜索功能"""

    index_models = [Bids]
    serializer_class = BidsIndexSerializer
    pagination_class = EnterprisePageNum

    def get_queryset(self, index_models=[]):
        """
        Get the list of items for this view.
        Returns ``self.queryset`` if defined and is a ``self.object_class``
        instance.

        @:param index_models: override `self.index_models`
        """
        if self.queryset is not None and isinstance(self.queryset, self.object_class):
            queryset = self.queryset.all().order_by("-CreateTime")
        else:
            queryset = self.object_class()._clone().order_by("-CreateTime")
            if len(index_models):
                queryset = queryset.models(*index_models)
            elif len(self.index_models):
                queryset = queryset.models(*self.index_models)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        列表获取
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data_dict_time = set()
        # 获取查询机
        queryset = self.filter_queryset(self.get_queryset())

        if queryset.count() == 0:
            return Response({
                'message': False,
            })

        try:
            page = self.paginate_queryset(queryset)
        except Exception as e:
            return Response({
                'state': False,
            })
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            names = locals()
            for article in serializer.data:
                data_dict_time.add(article['CreateTime'])

            data_list = list(serializer.data)
            data_ditc_content = {}

            for time in data_dict_time:
                i = 0
                names['list_%d' % i] = list()
                for article in data_list:
                    if time == article['CreateTime']:
                        # data_list.remove(article)
                        names['list_%s' % i].append(article)
                        article['CreateTime'] = time
                        data_ditc_content[time] = names['list_%s' % i]
                i += 1

            return Response({"content":data_ditc_content,"num":len(queryset)})
        return Response({"message": False})

    def retrieve(self, request, *args, **kwargs):
        return False

class RetrieveIndexView(HaystackViewSet):
    """实现搜索功能"""

    index_models = [Bids]
    serializer_class = RetrieveIndexSerializer
    pagination_class = EnterprisePageNum

    def retrieve(self, request, *args, **kwargs):
        """
        获取单篇文章
        """
        dict_data = request.query_params
        try:
            token = jwt_decode_handler(dict_data['token'])
            user = CustomerInformation.objects.get(id=token['user_id'])
        except Exception as e:
            return Response({"token_state":False})

        try:
            EnterpriseCertificationInfo.objects.get(user=user.id,identity_status=2)
        except:
            # 默认未关注  注销关注功能
            # is_collection = False

            # 获取redis
            collection = get_redis_connection('collection')
            # 获取查看次数
            begin_num = collection.get('collection_%s' % user.id)

            if begin_num == None:
                # 设置阅读数 / 要与认证功能结合 暂定
                collection.setex("collection_%s" % user.id, rest_of_day(), 1)
            else:
                # b类型转换
                begin_num = int(begin_num.decode())
                if begin_num >= 2:
                    return Response({
                        'message': False,
                    })
                else:
                    # 设置阅读数 / 要与认证功能结合 暂定
                    collection.setex("collection_%s" % user.id, rest_of_day(), begin_num + 1)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BidsSearchView(HaystackViewSet):
    """实现搜索功能"""

    index_models = [Bids]
    serializer_class = BidsIndexSerializer
    pagination_class = EnterprisePageNum


    def list(self, request, *args, **kwargs):
        dict_data = request.query_params
        try:
            # 用户
            token = jwt_decode_handler(dict_data['token'])
            user = CustomerInformation.objects.get(id=token['user_id'])
        except Exception as e:
            return Response({"token_state":False})
        # del request.query_params['token']
        # 获取查询机
        queryset = self.filter_queryset(self.get_queryset())

        if queryset.count()==0:
            return Response({
                'message': False,
            })

        keyword = request.query_params['Title']
        # 获取redis数据库
        history = get_redis_connection('history')
        history.zadd('keyword_%d' % user.id, 1, keyword)
        history.expire('keyword_%d' % user.id, 86400)

        # 设置有序集合
        text = history.zrangebyscore('keyword_%d' % user.id, 1, 2)

        try:
            page = self.paginate_queryset(queryset)
        except Exception as e:
            return Response({
                'state': False,
            })
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({"data_dict": serializer.data, "text": text, 'keyword': keyword,"number":len(queryset)})

        serializer = self.get_serializer(queryset, many=True)



        return Response({"data_dict": serializer.data, "text": text, 'keyword': keyword})

    def retrieve(self, request, *args, **kwargs):
        return False
        # article = Bids.objects.get(id=pk)
        # serializers = ArticledetailSerializer(article)
        # 是否可以访问
        # is_authentication = True
        # return Response({
        #     'is_authentication':is_authentication,
        #     "article": serializers.data,
        #     "message": "获取成功"
        # },status.HTTP_200_OK)


        # try:
        #     # 判断用户是否关注
        #     user.article.get(id=pk)
        # except Exception:
        #     # 不存在返回
        #     article = Bids.objects.filter(id=pk)
        #     serializers = ArticledetailSerializer(instance=article, many=True)
        #     return Response({
        #         # "is_collection": is_collection,
        #         "article": serializers.data,
        #         "message": "获取成功"
        #     })
        #
        # # 存在查询
        # article = user.article.filter(id=pk)
        # # is_collection = True
        # # 对象转字典
        # serializers = ArticledetailSerializer(instance=article, many=True)
        #
        # return Response({
        #     # "is_collection": is_collection,
        #     "article": serializers.data,
        #     "message": "获取成功"
        # })

class KeywordView(APIView):
    """
    快搜历史
    """
    def post(self,request):
        # user = User.objects.get(id=1)
        data_ditc = request.data
        try:
            token = jwt_decode_handler(data_ditc['token'])
            user = CustomerInformation.objects.get(id=token['user_id'])
        except Exception as e:
            return Response({"token_state":False})
        # 获取redis数据库
        history = get_redis_connection('history')
        # 设置有序集合
        text = history.zrangebyscore('keyword_%d' % user.id, 1, 2)
        # num = history.scard('keyword_%d' % user.id)
        # 判断是否有查询记录
        if not text:
            return Response({
                "message": False,
            })

        return Response({
            "history": text,
            "message": "返回成功",
        })
        # try:
        #     user = request.user
        # except Exception as e:
        #     user = None
        # if user and request.user.is_authenticated:
        #
        # else:
        #     return Response({
        #         "message": "未授权",
        #     })

    def delete(self, request):
        """删除数据"""
        # user = User.objects.get(id=1)
        data_ditc = request.data
        try:
            token = jwt_decode_handler(data_ditc['token'])
            user = CustomerInformation.objects.get(id=token['user_id'])
        except Exception as e:
            return Response({"token_state":False})

        # 获取redis数据库
        history = get_redis_connection('history')
        try:
            # 删除清空数据库
            history.zremrangebyrank('keyword_%d' % user.id, 0, -1)
        except Exception:
            return Response({
                "message": "还没有搜索噢~",
            })
        return Response({
            "message": "删除成功",
        })
        # try:
        #     user = request.user
        # except Exception as e:
        #     user = None
        # if user and request.user.is_authenticated:
        #
        # else:
        #     return Response({
        #         "message": "未授权",
        #     })
    def get(self,request):
        data_ditc = request.query_params
        # 用户获取
        token = jwt_decode_handler(data_ditc['token'])

        # 获取redis数据库
        history = get_redis_connection('history')
        try:
            # 设置有序集合
            text = history.zrangebyscore('keyword_%d' % token['user_id'], 1, 2)
        except Exception:
            return Response({
                "message": "没有数据",
            })
        return Response({"history": text,})
# class ArticledetailViews(GenericAPIView):
#     """
#     点击收藏
#     """
#     # permission_classes = [IsAuthenticated]
#
#     def get(self,request):
#         """
#         获取用户收藏文章
#         """
#         user = request.user
#         bids = user.article.all()
#         serializers = BidsSerializer(instance=bids, many=True)
#         return Response(serializers.data)
#
#     def post(self,request):
#         """
#         收藏添加/删除
#         """
#         user = request.user
#         data_dict = request.data
#
#         try:
#             article = Bids.objects.get(id=data_dict['id'])
#         except Exception as e:
#             return Response({
#                 "message": "服务器错误",
#             })
#
#         if not article:
#             return Response({
#                 "message": "没有该文章",
#             })
#
#         # 反向添加/删除
#         if data_dict['is_collection'] == True:
#             user.article.remove(article.id)
#         else:
#             user.article.add(article.id)
#
#         # 转成字典返回响应
#         return Response({
#             "message": "收藏成功",
#             # "is_collection": True,
#         },status.HTTP_201_CREATED)
#
#     def delete(self,request):
#         """
#         修改收藏
#         """
#         try:
#             user = User.objects.get(id=1)
#             # user = request.user
#         except Exception as e:
#             user = None
#         # 获取数据
#         dict_data = request.query_params
#         pk = dict_data['pk']
#         # 根据pk,查询是否关注
#         try:
#             # 判断用户是否关注
#             if int(pk) == 0: # 如果pk为0则删除所有
#                 bid = user.article.all()
#                 # 取消关注
#                 for i in bid:
#                     user.article.remove(i)
#             else:
#                 bid = user.article.get(id=dict_data['pk'])
#                 # 取消关注
#                 user.article.remove(bid)
#         except Exception:
#             # 不存在返回
#             return Response({
#                 "message": "未关注或文章已不存在"
#             })
#
#
#         # 4,转成字典,返回响应
#         return Response({
#                 "message": "取消成功"
#             })



# from .serializers import BidsIndexSerializer
# from drf_haystack.viewsets import HaystackViewSet
# class BidsearchViewSet(HaystackViewSet):
#     """
#     Bids搜索
#     """
#
#     index_models = [Bids]
#     serializer_class = BidsIndexSerializer
#     pagination_class = StandardPageNumberPagination


# class SubscriptionPush(APIView):
#     """
#     推送展示
#     """
#     def get(self,request):
#         # 测试用户
#         user = User.objects.get(id=1)
#         # user_serializer = UserSerializer(user)
#         bid = BidsUserSetting.objects.filter(mid=user.id)
#         if bid is None:
#             return Response({
#                 "message": "请设置关键字",
#             }, status.HTTP_202_ACCEPTED)
#
#         for keyword in keywords.split(","):
#             articles = Bids.objects.filter(Q(content__icontains=keyword) | Q(title__icontains=keyword),
#                                            create_time__gte=end_time, areas_id__in=list_area).exclude(
#                 id__in=id_dict)[begin_num:end＿num]
#             if articles.exists():
#                 serializer = FastSeekSerializer(articles, many=True)
#                 for article in serializer.data:
#                     # time = article.create_time
#                     bid_dict.append(article)
#                     id_dict.append(article['id'])

# class BidsSinglearticle(GenericAPIView,RetrieveModelMixin):
#     """
#     单篇文章获取
#     """
#     queryset = Bids.objects.all()
#     serializer_class = ArticledetailSerializer
#
#     def get(self, request, pk):
#         """
#         获取单篇文章
#         """
#         # 测试用户
#         # user = User.objects.get(id=1)
#         user = request.user
#         # 默认未关注  注销关注功能
#         # is_collection = False
#         # 获取redis
#         collection = get_redis_connection('collection')
#         # 获取查看次数
#         begin_num = collection.get('collection_%s' % user.id)
#
#         if begin_num == None:
#             # 设置阅读数 / 要与认证功能结合 暂定
#             collection.setex("collection_%s" % user.id, rest_of_day(), 1)
#         else:
#             # b类型转换
#             begin_num = int(begin_num.decode())
#             if begin_num >= 7:
#                 return Response({
#                     'is_authentication': False,
#                     "message": "已到上线,请认证",
#                 })
#             else:
#                 # 设置阅读数 / 要与认证功能结合 暂定
#                 collection.setex("collection_%s" % user.id, rest_of_day(), begin_num + 1)
#
#         return self.retrieve(request)

# class BidssearchView(APIView):
#     """
#     快搜搜索
#     """
#     def get(self,request):
#         """
#         搜索返回
#         """
#         try:
#             user = request.user
#         except Exception as e:
#             user = None
#         if user and request.user.is_authenticated:
#             # user = User.objects.get(id=1)
#
#             # 获取数据
#             data_dict = request.query_params
#             keyword = data_dict.get('keyword')
#             areas = data_dict.get('areas')
#             end_num = int(data_dict.get('end_num'))
#             # 设置懒加载条数
#             begin_num = end_num - 10
#
#             # 地区数据转换
#             areas_array = areas.split(",")
#             areas_dict = []
#             for areas in areas_array:
#                 areas_dict.append(int(areas))
#
#             if areas is None and keyword is not None:
#                 # 关键字查询
#                 articles = Bids.objects.filter(content__contains=keyword).order_by('-create_time')[begin_num:end_num]
#             elif keyword is None and areas is not None:
#                 articles = Bids.objects.filter(areas_id__in=areas).order_by('-create_time')[begin_num:end_num]
#             elif keyword is None and areas is None:
#                 articles = Bids.objects.all().order_by('-create_time')[begin_num:end_num]
#             else:
#
#                 from django.db.models import Q
#                 # 关键字查询
#                 articles = Bids.objects.filter(Q(content__icontains=keyword) | Q(title__icontains=keyword),
#                                                areas_id__in=areas_dict).order_by('-create_time')[begin_num:end_num]
#             serializers = FastSeekSerializer(instance=articles, many=True)
#             # 获取redis数据库
#             history = get_redis_connection('history')
#             history.zadd('keyword_%d' % user.id, 1, keyword)
#             history.expire('keyword_%d' % user.id, 86400)
#
#             # 设置有序集合
#             text = history.zrangebyscore('keyword_%d' % user.id, 1, 2)
#
#
#             return Response({
#                 "history": text,
#                 "keyword":keyword,
#                 "articles": serializers.data,
#                 "message": "成功",
#             }, status.HTTP_200_OK)
#
#         else:
#             return Response({
#                 "message": "未授权",
#             })
