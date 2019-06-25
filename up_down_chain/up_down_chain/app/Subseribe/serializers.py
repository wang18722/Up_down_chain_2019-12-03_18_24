from rest_framework import serializers

from .search_indexes import BidsIndex
from oauth.models import CustomerInformation
from .models import BidsUserSetting,Bids

# class ArticledetailSerializer(serializers.ModelSerializer):
#     """
#     内容展示
#     """
#
#     class Meta:
#         model = Bids
#         fields = "__all__"


class FastSeekSerializer(serializers.ModelSerializer):
    """
    快搜
    """
    class Meta:
        model = Bids
        fields = "__all__"



class KeywordSerializer(serializers.ModelSerializer):
    """
    关键词序列化器
    """


    class Meta:
        model = BidsUserSetting
        fields = "__all__"


# class UserSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=30, label="用户名")
#     image_url = serializers.CharField(max_length=200, label="t头像图片")
#     bids_set_id = serializers.PrimaryKeyRelatedField(label="关键词设置",read_only=True)
#
#     class Meta:
#         model = CustomerInformation
#         fields = "__all__"


from drf_haystack.serializers import HaystackSerializer
class BidsIndexSerializer(HaystackSerializer):
    """
    Bids索引结果数据序列化器

    """
    # 'BidsAreaID',
    class Meta:
        index_classes = [BidsIndex]
        fields = ('BidsAreaID','id','EndDate','CreateTime','Url','Company','ReleaseDate','IsDeleted','IsValid','Title','BidsPirce')

class RetrieveIndexSerializer(HaystackSerializer):
    """
    RetrieveIndex索引结果数据序列化器

    """
    class Meta:
        index_classes = [BidsIndex]
        fields = ('BidsContent',)
