from rest_framework import serializers
from .models import BidsUserSetting,Bids
from .query_indexs import BidsIndex
from drf_haystack.serializers import HaystackSerializer

class RemindInfoSerializer(serializers.Serializer):

    class Meta:
        model = BidsUserSetting
        exclude = ('create_time','update_time')



class BidsIndexSerializer(HaystackSerializer):
    """
    Bids索引结果数据序列化器

    """
    RemindInfoSerializer(read_only=True)

    class Meta:
        index_classes = [BidsIndex]
        fields = ('company', 'id', 'name', 'price', 'title', 'source','url','areas_id','content')