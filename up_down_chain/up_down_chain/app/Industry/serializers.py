from drf_haystack.serializers import HaystackSerializer
from .search_indexes import *


class PreciseRetrievalSerializer(HaystackSerializer):
    """
    索引结果序列化器
    检查前端传入的参数text，并且检索出数据后再使用这个序列化器返回给前端
    """

    # 向前端返回数据时序列化的字段
    # Haystack通过Elasticsearch检索出搜索结果后，
    # 会在数据库中取出完整的数据库模型类对象，放到object中
    # 序列化器可改


    class Meta:
        # 索引类名称可改
        index_classes = [ANlmyIndex,BCkyIndex,FPflsyIndex,GJcyIndex,CZzyIndex,DDrrsgyIndex,EJzyIndex,FPflsyIndex,GJcyIndex,HZscyyIndex,IXxrjyIndex,JJryIndex,KFdcyIndex,LZlswIndex,MKyjsIndex,NSlhjggIndex,OJmxlIndex,PJyIndex,QWsshIndex,RWtyIndex,SGgshIndex]

        fields = ("phone","company_name","industry_involved","province","industries")


class RecommendedIndexSerializer(HaystackSerializer):
    """
    索引结果序列化器
    检查前端传入的参数text，并且检索出数据后再使用这个序列化器返回给前端
    """

    # 向前端返回数据时序列化的字段
    # Haystack通过Elasticsearch检索出搜索结果后，
    # 会在数据库中取出完整的数据库模型类对象，放到object中
    # 序列化器可改
    # object = RSerializer()

    class Meta:
        # 索引类名称可改
        index_classes = [ANlmyIndex,BCkyIndex,FPflsyIndex,GJcyIndex,CZzyIndex,DDrrsgyIndex,EJzyIndex,FPflsyIndex,GJcyIndex,HZscyyIndex,IXxrjyIndex,JJryIndex,KFdcyIndex,LZlswIndex,MKyjsIndex,NSlhjggIndex,OJmxlIndex,PJyIndex,QWsshIndex,RWtyIndex,SGgshIndex]

        fields = ("company_name","company_id","industriesid")