from rest_framework import serializers
from .models import BidsUserSetting,Bids,ArticledetailModel
# from .search_indexes import BidsIndex
# from drf_haystack.serializers import HaystackSerializer

class RemindInfoSerializer(serializers.Serializer):

    class Meta:
        model = BidsUserSetting
        exclude = ('create_time','update_time')


class BidsSerializer(serializers.Serializer):
    """
    推送内容
    """
    pirce = serializers.DecimalField(max_digits=10, decimal_places=2, label='单价',read_only=True)
    id = serializers.IntegerField(label="ID",read_only=True)
    company = serializers.CharField(max_length=100, label="公司",read_only=True)
    isValid = serializers.BooleanField( label="是否有效",read_only=True)
    title = serializers.CharField(label='名字', max_length=100,read_only=True)
    create_time = serializers.DateTimeField(label="时间")
    by_time = serializers.DateTimeField(label="截止时间")

    class Meta:
        model = Bids
        exclude = ('update_time')


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
    create_time = serializers.DateTimeField(label="时间")
    by_time = serializers.DateTimeField(label="截止时间")

    class Meta:
        model = Bids
        exclude = ('update_time')

class Articlecollection(serializers.ModelSerializer):

    class Meta:
        model = ArticledetailModel
        fields = ("mid","bids_id")

    def update(self, instance, validated_data):
        """
        修改关注状态
        """

        bids_id = validated_data['is_collection']
        instance.focus = bids_id
        instance.save()

        return instance

    # def create(self, validated_data):
# class BidsIndexSerializer(HaystackSerializer):
#     """
#     Bids索引结果数据序列化器
#
#     """
#     # RemindInfoSerializer(read_only=True)
#
#     class Meta:
#         index_classes = [BidsIndex]
#         fields = ('company', 'id', 'name', 'price', 'title', 'source','url','areas_id','content')