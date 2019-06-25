from drf_haystack.viewsets import HaystackViewSet
from rest_framework.response import Response

from .utils import EnterprisePageNum
from .models import *
from .serializers import RecommendedIndexSerializer, PreciseRetrievalSerializer


class SearchView(HaystackViewSet):
    """实现搜索功能"""

    # 模型类可改

    index_models = [ANlmy, BCky, CZzy, DDrrsgy, EJzy, FPflsy, GJcy, HZscyy, IXxrjy, JJry, KFdcy, LZlsw, MKyjs, NSlhjgg,
                    OJmxl, PJy, QWssh, RWty, SGgsh]
    serializer_class = RecommendedIndexSerializer
    pagination_class = EnterprisePageNum


class PreciseRetrievalView(HaystackViewSet):
    """精准搜索使用ES"""

    index_models = [ANlmy, BCky, CZzy, DDrrsgy, EJzy, FPflsy, GJcy, HZscyy, IXxrjy, JJry, KFdcy, LZlsw, MKyjs, NSlhjgg,
                    OJmxl, PJy, QWssh, RWty, SGgsh]

    serializer_class = PreciseRetrievalSerializer

    pagination_class = EnterprisePageNum

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        list_data = serializer.data
        list_obj_data=[]
        for data in list_data:
            dict_data={}
            # print(data)
            if data["phone"]:
                dict_data["phone"] = data["phone"][:7] + "****"
                dict_data["company_name"] = data["company_name"]
                dict_data["industry_involved"] = data["industry_involved"]
                dict_data["province"] = data["province"]
            # print(dict_data)
                list_obj_data.append(dict_data)

        # print(list_obj_data)
        return Response(list_obj_data)