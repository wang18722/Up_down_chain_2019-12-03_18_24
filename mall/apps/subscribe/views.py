import re
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from areas.models import Area
from utils.endtoday import rest_of_day
from .serializers import BidsSerializer, BidsIndexSerializer, Articlecollection
from .models import Bids, User
from django_redis import get_redis_connection
from drf_haystack.viewsets import HaystackViewSet

class RemindInfoViews(APIView):
    """
    关键词设置
    """
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        bids_set = user.bids_set_id
        # keywords_array = bids_set.keywords_array.split(",")
        areas_array = bids_set.areas_id.split(",")

        if bids_set is None or bids_set.areas_id is None:
            return Response({
                'user': user,
                # 'bids_set':bids_set,
                'areas_dict': [0],
            })

        areas_dict = []
        for areas in areas_array:
            area = Area.objects.filter(id=areas)
            areas_dict.append(area)

        keywords = bids_set.keywords_array.split(",")
        areas = bids_set.areas_id

        return Response({
            'user': user,
            "keywords":keywords,
            'areas':areas,
            'areas_dict':areas_dict,
        })

    def put(self,request):
        # 获取前端数据
        dict_data = request.query_params

        areas_dict = dict_data.get('areas_dict')
        keywords_array = dict_data.get('keywords_array')
        is_remind =dict_data.get('is_remind')
        remind_long_time = dict_data.get('remind_long_time')

        user = request.user
        # 判断关键字是否包含特殊字符
        for keyword in keywords_array:
            if bool(re.search('\W+', keyword)) or 2 > len(keyword) >= 7 :
                return Response({"message":"关键词不能包含特殊字符或者超过2-6个字,请修改后保存"}, status=status.HTTP_404_NOT_FOUND)

        # 把地区列表转换为字符串
        areas_str = ','.join(areas_dict)
        try:
            user.bids_set_id.update(areas_id=areas_str,keywords_array=keywords_array,remind_long_time=remind_long_time,is_remind=is_remind)
        except Exception:
            return Response({
                "message": "修改失败,服务器异常"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message":"保存成功",
            })

class BidsSearchViewSet(APIView):
    """
    推送展示
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,areas,keywords):

        try:
            user = request.user
        except Exception as e:
            user = None
        if user and request.user.is_authenticated:
            bids_set = user.bids_set_id
            if bids_set is None:
                return Response({
                    "message": "请设置关键字",
                })
            else:
                # 定义文章字典
                bid_dict = []
                #　文章id列表
                id_dict = []
                remind_time = request.user.bids_set_id.remind_long_time
                end＿num = request.query_params.get('num')

                # 把地区编号转为列表
                list_area = list(eval(areas))
                begin_num = end＿num-10
                import datetime
                def get_date(days=7):
                    return datetime.datetime.now() - datetime.timedelta(days=days)

                for keyword in keywords.split(","):
                    articles = Bids.objects.filter(content__contains=keyword, create_time__gte=get_date(days=remind_time),areas_id__in=list_area).exclude(id__in=id_dict).order_by('-create_time')[begin_num:end＿num]
                    if articles.exists():
                        serializer = BidsSerializer(instance=articles, many=True)
                        for article in serializer.data:
                            time = re.match("(.+)T", article['create_time']).group(1)
                            bid_dict.append({time: article})
                            id_dict.append(article['id'])
                return Response({
                    "bid_dict": bid_dict
                })
        else:
            return Response({
                "message": "未授权",
            })

class BidsSinglearticle(APIView):
    """
    单篇文章获取
    """

    def get(self, request):
        """
        获取单篇文章
        """

        user = request.user
        pk = request.query_params.get('pk')
        # user = User.objects.get(id=1)
        # 默认未关注
        is_collection = False
        # 获取redis
        collection = get_redis_connection('collection')
        # 获取查看次数
        begin_num = collection.get('collection_%s' % user.id)

        if begin_num == None:
            # 设置阅读数 / 要与认证功能结合 暂定
            collection.setex("collection_%s" % user.id, rest_of_day(), 1)

        # b类型转换
        begin_num = int(begin_num.decode())
        if begin_num >= 100:
            return Response({
                "message": "已到上线,请认证",
            })
        else:
            # 设置阅读数 / 要与认证功能结合 暂定
            collection.setex("collection_%s" % user.id, rest_of_day(), begin_num + 1)

        try:
            # 判断用户是否关注
            user.article.get(id=pk)
        except Exception:
            # 不存在返回
            article = Bids.objects.filter(id=pk)
            serializers = BidsSerializer(instance=article, many=True)
            return Response({
                "is_collection": is_collection,
                "article": serializers.data,
                "message": "获取成功"
            })

        # 存在查询
        article = user.article.filter(id=pk)
        is_collection = True
        # 对象转字典
        serializers = BidsSerializer(instance=article, many=True)

        return Response({
            "is_collection": is_collection,
            "article": serializers.data,
            "message": "获取成功"
        })

# class ArticledetailViews(RetrieveUpdateAPIView):
#     # queryset = Bids.objects.all()
#     serializer_class = ArticledetailSerializer
#
#     def get_queryset(self):
#         return Bids.objects.filter(id=self.request.query_params.get('id'))
#
#     def get(self, request, *args, **kwargs):
#         try:
#             user = request.user
#         except Exception as e:
#             user = None
#         artic_id = kwargs['id']
#         is_collected = False
#         if user



class ArticledetailViews(GenericAPIView):
    """
    点击收藏
    """
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        """
        获取用户收藏文章
        """
        user = request.user
        bids = user.article.all()
        serializers = BidsSerializer(instance=bids, many=True)
        return Response(serializers.data)

    def post(self,request):
        """
        收藏添加/删除
        """
        user = request.user
        data_dict = request.data

        try:
            article = Bids.objects.get(id=data_dict['id'])
        except Exception as e:
            return Response({
                "message": "服务器错误",
            })

        if not article:
            return Response({
                "message": "没有该文章",
            })

        # 反向添加/删除
        if data_dict['is_collection'] == True:
            user.article.remove(article.id)
        else:
            user.article.add(article.id)

        # 转成字典返回响应
        return Response({
            "message": "收藏成功",
            # "is_collection": True,
        },status.HTTP_201_CREATED)

    def delete(self,request):
        """
        修改收藏
        """
        try:
            user = User.objects.get(id=1)
            # user = request.user
        except Exception as e:
            user = None
        # 获取数据
        dict_data = request.query_params
        pk = dict_data['pk']
        # 根据pk,查询是否关注
        try:
            # 判断用户是否关注
            if int(pk) == 0: # 如果pk为0则删除所有
                bid = user.article.all()
                # 取消关注
                for i in bid:
                    user.article.remove(i)
            else:
                bid = user.article.get(id=dict_data['pk'])
                # 取消关注
                user.article.remove(bid)
        except Exception:
            # 不存在返回
            return Response({
                "message": "未关注或文章已不存在"
            })


        # 4,转成字典,返回响应
        return Response({
                "message": "取消成功"
            })




class SKUSearchViewSet(HaystackViewSet):
    """
    Bids搜索
    """

    index_models = [Bids]
    serializer_class = BidsIndexSerializer
