from rest_framework import serializers
from .models import BidsUserSetting,Bids,User
from .search_indexes import BidsIndex
from drf_haystack.serializers import HaystackSerializer

# class RemindInfoSerializer(serializers.Serializer):
#
#     class Meta:
#         model = BidsUserSetting
#         exclude = ('create_time','update_time')


class BidsSerializer(serializers.Serializer):
    """
    推送内容
    """
    pirce = serializers.DecimalField(max_digits=10, decimal_places=2, label='单价',read_only=True)
    id = serializers.IntegerField(label="ID",read_only=True)
    company = serializers.CharField(max_length=100, label="公司",read_only=True)
    isValid = serializers.BooleanField( label="是否有效",read_only=True)
    title = serializers.CharField(label='名字', max_length=100,read_only=True)
    by_time = serializers.DateTimeField(label="截止时间")

    class Meta:
        model = Bids
        exclude = ('update_time','create_time')


class ArticledetailSerializer(serializers.ModelSerializer):
    """
    内容展示
    """
    pirce = serializers.DecimalField(max_digits=10, decimal_places=2, label='单价', read_only=True)
    id = serializers.IntegerField(label="ID", read_only=True)
    company = serializers.CharField(max_length=100, label="公司", read_only=True)
    content = serializers.CharField(label="文章内容", read_only=True)
    isValid = serializers.BooleanField(label="是否有效", read_only=True)
    title = serializers.CharField(label='名字', max_length=100, read_only=True)
    by_time = serializers.DateTimeField(label="截止时间")

    class Meta:
        model = Bids
        exclude = ('update_time','create_time')

class Articlecollection(serializers.ModelSerializer):
    pirce = serializers.DecimalField(max_digits=10, decimal_places=2, label='单价', read_only=True)
    id = serializers.IntegerField(label="ID", read_only=True)
    company = serializers.CharField(max_length=100, label="公司", read_only=True)
    isValid = serializers.BooleanField(label="是否有效", read_only=True)
    title = serializers.CharField(label='名字', max_length=100, read_only=True)
    by_time = serializers.DateTimeField(label="截止时间")

    class Meta:
        model = Bids
        exclude = ('update_time','create_time')



class BidsIndexSerializer(HaystackSerializer):
    """
    Bids索引结果数据序列化器

    """
    # RemindInfoSerializer(read_only=True)

    class Meta:
        index_classes = [BidsIndex]
        fields = ('company', 'id', 'name', 'price', 'title', 'source','url','areas_id','content')