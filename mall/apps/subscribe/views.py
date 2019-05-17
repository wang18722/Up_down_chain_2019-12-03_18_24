import re
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView,ListAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from areas.models import Area
from .serializers import BidsSerializer, ArticledetailSerializer, Articlecollection
from .models import Bids, ArticledetailModel
# from .serializers import BidsIndexSerializer
# from drf_haystack.viewsets import HaystackViewSet

class RemindInfoViews(APIView):

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
        dict_data = request.query_params.dict()

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

class ArticledetailViews(APIView):
    """
    点击收藏
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        """
        获取单篇文章
        """
        user = request.user
        bid = Bids.objects.get(id=pk)
        is_collection = False
        coollection = ArticledetailModel.objects.filder(bids_id=bid.id,mid=user.id,focus=True)
        if coollection.exists():
            is_collection = True
        # 对象转字典
        serializer = ArticledetailSerializer(bid,many=True)
        # print(serializer)

        # 返回响应
        return Response({
            "is_collection":is_collection,
            "article":serializer,
            "message": "获取成功"
        })

    def post(self,request):
        """
        收藏
        :param request:
        :return:
        """

        data_dict = request.data

        # 创建关注
        serializer = Articlecollection(data=data_dict)
        serializer.is_valid(raise_exception=True)

        # 数据入库
        serializer.save()

        # 转成字典返回响应
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    # def put(self,request,pk):
    #     """
    #     修改收藏
    #     """
    #     try:
    #         user = request.user
    #     except Exception as e:
    #         user = None
    #     # 获取数据
    #     dict_data = request.data
    #
    #     # 根据pk,查询是否关注
    #     article = ArticledetailModel.objects.filder(bids_id=pk,mid=user.id)
    #
    #     # 判断是否已关注
    #     if article.exists() and article.is_collection:
    #         return self.post(request,pk)
    #
    #     # 修改关注
    #     serializer = Articlecollection(instance=article, data=dict_data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     # 4,转成字典,返回响应
    #     return Response(serializer.validated_data)

# class SKUSearchViewSet(HaystackViewSet):
#     """
#     Bids搜索
#     """
#
#     index_models = [Bids]
#     serializer_class = BidsIndexSerializer




