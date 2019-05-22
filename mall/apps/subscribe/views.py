import re
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.endtoday import rest_of_day
from .serializers import  KeywordSerializer, FastSeekSerializer,ArticledetailSerializer
from .models import Bids, User, BidsUserSetting
from django_redis import get_redis_connection
# from drf_haystack.viewsets import HaystackViewSet

class RemindInfoViews(GenericAPIView):
    """
    关键词设置
    """
    serializer_class = KeywordSerializer
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        # user = request.user
        # 测试用户
        user = User.objects.get(id=1)
        # user_serializer = UserSerializer(user)
        bid = BidsUserSetting.objects.filter(mid=user.id)

        if bid is None:
            return Response({
                "message": "请设置关键字",
            },status.HTTP_202_ACCEPTED)

        # bid = BidsUserSetting.objects.get(id=bid_set_id)
        bid_serializer =self.get_serializer(instance=bid,many=True)

        # 关键词不转换 看前端
        # keywords_array = bids_set.keywords_array.split(",")
        # areas_array = bids_set.areas_id.split(",")
        #
        # areas_dict = []
        # for areas in areas_array:
        #     area = Area.objects.filter(id=areas)
        #     areas_dict.append(area)
        #
        # keywords = bids_set.keywords_array.split(",")
        # areas = bids_set.areas_id

        return Response(
            # 'user_name': user.name,
            # 'user_image_url': user.image_url,
            bid_serializer.data)

    def post(self,request):
        """
        关键词设置
        """

        try:
            user = request.user
        except Exception as e:
            user = None
        if user and request.user.is_authenticated:
            # 获取前端数据
            dict_data = request.data
            keywords_array = dict_data.get('keywords_array')

            # 判断关键字是否包含特殊字符
            for keyword in keywords_array.split(","):
                if bool(re.search('\W+', keyword)) or 2 > len(keyword) >= 7:
                    return Response({"message": "关键词不能包含特殊字符或者超过2-6个字,请修改后保存"}, status=status.HTTP_404_NOT_FOUND)
            try:
                bid = BidsUserSetting.objects.get(mid_id=user.id)
                serializer = self.get_serializer(instance=bid, data=dict_data)
            except Exception:
                # 没有该对象则创建
                serializer = self.get_serializer(data=dict_data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "保存成功",
            })
        return Response({
            "message": "用户不存在",
        })

class BidsSearchViewSet(APIView):
    """
    推送筛选
    """
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        # user = User.objects.get(id=1)

        try:
            user = request.user
        except Exception as e:
            user = None
        if user and request.user.is_authenticated:
            try:
                bid = BidsUserSetting.objects.get(mid=user.id)
            except Exception:
                return Response({
                    "message": "请设置关键字",
                })
            else:
                data_ditc = request.query_params
                # 定义文章字典
                bid_dict = []
                # 　文章id列表
                id_dict = []

                # 推送时常
                remind_time = int(bid.remind_long_time) * 86400
                # 数据类型转换
                end＿num = int(data_ditc.get('num'))
                areas = data_ditc.get('areas')
                keywords = data_ditc.get('keywords')

                # 判断是否为空,若是空则去数据库查找
                if keywords is None and areas is None:
                    keywords = bid.keywords
                    areas = bid.areas

                # 懒加载开始条数
                begin_num = end＿num - 10
                import time
                # 推送时间计算
                end_time = time.strftime('%Y-%m-%d', time.localtime(time.time() - remind_time))
                from django.db.models import Q  # 框架原因手动导入Q
                if areas == '0':
                    for keyword in keywords.split(","):
                        # 　过滤查询
                        articles = Bids.objects.filter(Q(content__icontains=keyword) | Q(title__icontains=keyword),
                                                       create_time__gte=end_time).exclude(
                            id__in=id_dict)[begin_num:end＿num]
                        if articles.exists():  # 判断是否存在queryset
                            serializer = FastSeekSerializer(articles, many=True)
                            for article in serializer.data:
                                # time = article.create_time
                                bid_dict.append(article)
                                id_dict.append(article['id'])  # 防止重复数据
                else:
                    # 把地区编号转为列表
                    list_area = areas.split(",")
                    for keyword in keywords.split(","):
                        # 　过滤查询
                        articles = Bids.objects.filter(Q(content__icontains=keyword) | Q(title__icontains=keyword),
                                                       create_time__gte=end_time, areas_id__in=list_area).exclude(
                            id__in=id_dict)[begin_num:end＿num]
                        if articles.exists():  # 判断是否存在queryset
                            serializer = FastSeekSerializer(articles, many=True)
                            for article in serializer.data:
                                # time = article.create_time
                                bid_dict.append(article)
                                id_dict.append(article['id'])  # 防止重复数据
                return Response({
                    "message": "查询成功",
                    "bid_dict": bid_dict
                })
        else:
            return Response({
                "message": "未授权",
            })

class BidsSinglearticle(GenericAPIView,RetrieveModelMixin):
    """
    单篇文章获取
    """
    queryset = Bids.objects.all()
    serializer_class = ArticledetailSerializer
    def get(self, request, pk):
        """
        获取单篇文章
        """
        # 测试用户
        user = User.objects.get(id=1)
        # user = request.user
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
            if begin_num >= 7:
                return Response({
                    'is_authentication': False,
                    "message": "已到上线,请认证",
                })
            else:
                # 设置阅读数 / 要与认证功能结合 暂定
                collection.setex("collection_%s" % user.id, rest_of_day(), begin_num + 1)

        return self.retrieve(request)

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

class BidssearchView(APIView):
    """
    快搜搜索
    """
    def get(self,request):
        """
        搜索返回
        """
        try:
            user = request.user
        except Exception as e:
            user = None
        if user and request.user.is_authenticated:
            # user = User.objects.get(id=1)

            # 获取数据
            data_dict = request.query_params
            keyword = data_dict.get('keyword')
            areas = data_dict.get('areas')
            end_num = int(data_dict.get('end_num'))
            # 设置懒加载条数
            begin_num = end_num - 10

            # 地区数据转换
            areas_array = areas.split(",")
            areas_dict = []
            for areas in areas_array:
                areas_dict.append(int(areas))

            if areas is None and keyword is not None:
                # 关键字查询
                articles = Bids.objects.filter(content__contains=keyword).order_by('-create_time')[begin_num:end_num]
            elif keyword is None and areas is not None:
                articles = Bids.objects.filter(areas_id__in=areas).order_by('-create_time')[begin_num:end_num]
            elif keyword is None and areas is None:
                articles = Bids.objects.all().order_by('-create_time')[begin_num:end_num]
            else:

                from django.db.models import Q
                # 关键字查询
                articles = Bids.objects.filter(Q(content__icontains=keyword) | Q(title__icontains=keyword),
                                               areas_id__in=areas_dict).order_by('-create_time')[begin_num:end_num]
            serializers = FastSeekSerializer(instance=articles, many=True)
            # 获取redis数据库
            history = get_redis_connection('history')
            history.zadd('keyword_%d' % user.id, 1, keyword)
            history.expire('keyword_%d' % user.id, 86400)

            # 设置有序集合
            text = history.zrangebyscore('keyword_%d' % user.id, 1, 2)


            return Response({
                "history": text,
                "keyword":keyword,
                "articles": serializers.data,
                "message": "成功",
            }, status.HTTP_200_OK)

        else:
            return Response({
                "message": "未授权",
            })

class KeywordView(APIView):
    """
    点击快搜
    """
    def get(self,request):

        try:
            user = request.user
        except Exception as e:
            user = None
        if user and request.user.is_authenticated:
            user = User.objects.get(id=1)
            # 获取redis数据库
            history = get_redis_connection('history')
            # 设置有序集合
            text = history.zrangebyscore('keyword_%d' % user.id, 1, 2)
            # num = history.scard('keyword_%d' % user.id)
            # 判断是否有查询记录
            if text is None:
                bids_set = BidsUserSetting.objects.get(id=user.bids_set_id_id)
                text = bids_set.keywords_array.split(",")

            return Response({
                "history": text,
                "message": "返回成功",
            })
        else:
            return Response({
                "message": "未授权",
            })

    def delete(self, request):
        """删除数据"""

        try:
            user = request.user
        except Exception as e:
            user = None
        if user and request.user.is_authenticated:
            user = User.objects.get(id=1)
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
        else:
            return Response({
                "message": "未授权",
            })

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




# class SKUSearchViewSet(HaystackViewSet):
#     """
#     Bids搜索
#     """
#
#     index_models = [Bids]
#     serializer_class = BidsIndexSerializer

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