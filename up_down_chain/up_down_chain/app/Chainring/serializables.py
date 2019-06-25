from rest_framework import serializers

from Chainring.models import Grouping, Associated
from Enterprise.models import EnterpriseInformationForCustomer


class GroupingSerializer(serializers.ModelSerializer):
    """分组序列化器"""

    class Meta:
        model = Grouping
        fields = ("grouping",)

class EnterpriseSerializer(serializers.ModelSerializer):
    """分组序列化器"""

    class Meta:
        # model = EnterpriseModel
        fields = ("enterprises",)



class AssociatedSerializer(serializers.ModelSerializer):
    """关注和取消关注功能"""

    class Meta:
        model = Associated
        fields = ("focus",)

    def update(self, instance, validated_data):
        """更新关注状态功能"""
        # 遍历字符集索引
        # validated_data只获取到一个状态
        for index in range(len(instance)):
            print(index)
            # 保存更改的对象
            instance[index].focus = validated_data.get("focus", instance[index].focus)

            # save保存操作
            instance[index].save()

        return instance


class SelfPortraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseInformationForCustomer
        fields = "__all__"


class PreciseRetrievalSerializer(serializers.ModelSerializer):
    """精准检索"""