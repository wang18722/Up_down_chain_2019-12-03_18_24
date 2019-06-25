
from rest_framework import serializers

from Enterprise.utils import value
from Users.models import EnterpriseCertificationInfo

from .models import Enterprises, Function, Chain, DatasummaryForUp, Datasummary, Provinces


class ListSerializer(serializers.ModelSerializer):
    """列表"""

    class Meta:

        model =Function
        fields = ("company_name", "id")


class DefaultSerializer(serializers.ModelSerializer):
    """首页功能"""


    class Meta:
        model = Function
        fields = "__all__"


    def create(self, validated_data):
        """保存操作"""
        print(validated_data)
        obj = Function.objects.create(**validated_data)

        return obj

    def update(self, instance, validated_data):
        """更新操作"""
        # print(instance[0])
        print(validated_data)

        # 如果是推荐,则需要更新两个表:推荐状态 和 推荐数+1
        # instance传回的是对象,validated_data要更新的数据
        i = instance[0]
        if validated_data["default_page"] == True:
            i.default_page = validated_data["default_page"]
            i.save()
            return i
        else:
            i.default_page = validated_data["default_page"]
            i.save()
            return i


class RecommendedSerializer(serializers.ModelSerializer):
    """我推荐"""
    class Meta:
        model = Function
        fields = "__all__"

    def create(self, validated_data):
        """保存操作"""
        obj = Function.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        """更新操作"""

        # 如果是推荐,则需要更新两个表:推荐状态 和 推荐数+1
        # instance传回的是对象,validated_data要更新的数据
        i = instance[0]
        if validated_data["i_recommend"] == True:
            i.i_recommend = validated_data["i_recommend"]
            i.save()
            return i
        else:
            i.i_recommend = validated_data["i_recommend"]
            i.save()
            return i



#

class AreaSerializer(serializers.ModelSerializer):
    """
    行政区划信息序列化器
    """
    class Meta:
        model = Provinces
        fields = ('id', 'provinces')



class SingleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Datasummary
        fields = ("industry","province","amount")

class SingleUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = DatasummaryForUp
        fields = ("industry", "province", "amount")

# class MatchingInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OauthQYUser
#         fields = ('id','demand_config')
#
# class MarketingprovincesSerializer(serializers.ModelSerializer):
#     weidu = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='industry'
#     )
#     areas = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='provinces'
#     )
#     class Meta:
#         model = OauthQYUser
#         filter = ('id')


class AndustrySerializer(serializers.ModelSerializer):
    """
    行业信息序列化器
    """
    class Meta:
        model = Chain
        fields = ('id', 'industry')


class MatchingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseCertificationInfo
        fields = ('id','demand_config')

class MarketingprovincesSerializer(serializers.ModelSerializer):
    weidu = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='industry'
    )
    areas = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='provinces'
    )
    class Meta:
        model = EnterpriseCertificationInfo
        filter = ('id')
