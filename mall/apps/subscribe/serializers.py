from rest_framework import serializers
from .models import BidsUserSetting,Bids,User
# from .search_indexes import BidsIndex
from drf_haystack.serializers import HaystackSerializer
from django.db import models
# class RemindInfoSerializer(serializers.Serializer):
#
#     class Meta:
#         model = BidsUserSetting
#         exclude = ('create_time','update_time')


# class BidsSerializer(serializers.ModelSerializer):
#     """
#     推送内容
#     """
#     # pirce = serializers.DecimalField(max_digits=10, decimal_places=2, label='单价',read_only=True)
#     # id = serializers.IntegerField(label="ID",read_only=True)
#     # company = serializers.CharField(max_length=100, label="公司",read_only=True)
#     # isValid = serializers.BooleanField( label="是否有效",read_only=True)
#     # title = serializers.CharField(label='名字', max_length=100,read_only=True)
#     # by_time = serializers.DateTimeField(label="截止时间")
#
#     class Meta:
#         model = Bids
#         fields = ('pirce', 'id', 'company', 'isValid', 'title', 'by_time')


class ArticledetailSerializer(serializers.ModelSerializer):
    """
    内容展示
    """
    # pirce = serializers.DecimalField(max_digits=10, decimal_places=2, label='单价', read_only=True)
    # id = serializers.IntegerField(label="ID", read_only=True)
    # company = serializers.CharField(max_length=100, label="公司", read_only=True)
    # content = serializers.CharField(label="文章内容", read_only=True)
    # isValid = serializers.BooleanField(label="是否有效", read_only=True)
    # title = serializers.CharField(label='名字', max_length=100, read_only=True)
    # by_time = serializers.DateTimeField(label="截止时间")

    class Meta:
        model = Bids
        fields = ('pirce', 'id', 'company', 'isValid', 'title', 'by_time', 'create_time','content')

class Articlecollection(serializers.ModelSerializer):
    # pirce = serializers.DecimalField(max_digits=10, decimal_places=2, label='单价', read_only=True)
    # id = serializers.IntegerField(label="ID", read_only=True)
    # company = serializers.CharField(max_length=100, label="公司", read_only=True)
    # isValid = serializers.BooleanField(label="是否有效", read_only=True)
    # title = serializers.CharField(label='名字', max_length=100, read_only=True)
    # by_time = serializers.DateTimeField(label="截止时间")

    class Meta:
        model = Bids
        exclude = ('update_time','create_time')

class FastSeekSerializer(serializers.ModelSerializer):
    """
    快搜
    """
    class Meta:
        model = Bids
        fields = ('pirce','id','company','isValid','title','by_time','create_time')



class KeywordSerializer(serializers.ModelSerializer):
    """
    关键词序列化器
    """
    id = serializers.IntegerField(label='ID',read_only=True)
    areas_id = serializers.CharField(max_length=60, label="关注省范围")
    keywords_array = serializers.CharField(max_length=60, label="关注关键字")
    remind_long_time = serializers.IntegerField(default=7, label="推送时常")
    is_remind = serializers.BooleanField(default=True, label="是否推送")

    class Meta:
        model = BidsUserSetting
        fields = ('id','areas_id','keywords_array','remind_long_time','is_remind')
        # extra_kwargs = {
        #     'id': {'read_only': True},
        # }
    # def update(self, instance, validated_data):
    #     instance.areas_id = validated_data.get('areas_id')
    #     instance.keywords_array = validated_data.get('keywords_array')
    #     instance.remind_long_time = validated_data.get('remind_long_time')
    #     instance.is_remind = validated_data.get('is_remind')

class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, label="用户名")
    image_url = serializers.CharField(max_length=200, label="t头像图片")
    bids_set_id = serializers.PrimaryKeyRelatedField(label="关键词设置",read_only=True)

    class Meta:
        model = User
        fields = "__all__"

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