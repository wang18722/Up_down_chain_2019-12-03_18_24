import re
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from areas.models import Area
from subscribe.models import Bids
from .serializers import BidsIndexSerializer
from drf_haystack.viewsets import HaystackViewSet

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

        # keywords = bids_set.keywords_array
        # areas = bids_set.areas_id

        return Response({
            'user': user,
            # "keywords":keywords,
            # 'areas':areas,
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

# class RemindArticle(APIView):
#     # pagination_class = None
#     def get(self,request):
#         try:
#             user = request.user
#         except Exception as e:
#             user = None
#         if user and request.user.is_authenticated:
#             bids_set = user.bids_set_id
#             if bids_set is None:
#                 return Response({
#                     "message": "请设置关键字",
#                 })
#             else:
#                 pass
#         else:
#             return Response({
#                 "message": "未授权",
#             })


class SKUSearchViewSet(HaystackViewSet):
    """
    Bids搜索
    """

    index_models = [Bids]
    serializer_class = BidsIndexSerializer
