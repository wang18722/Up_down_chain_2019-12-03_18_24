from rest_framework import serializers
from Users.models import Top_up_Payment
from oauth.models import OAuthWXUser
from .models import OrderInfo,RechargeModel, SmsCallback


class PaySerializers(serializers.ModelSerializer):
    """
    支付序列化器
     """

    class Meta:
        model = OrderInfo
        fields = "__all__"

class RechargeSerializers(serializers.ModelSerializer):
    """
    充值记录
    """
    class Meta:
        model = RechargeModel
        fields = "__all__"
    def update(self, instance, validated_data):
        instance.pay_state = validated_data.get("pay_state",instance.pay_state)
        instance.save()

        return instance
class PaymentSerializers(serializers.ModelSerializer):
    """
    充值
    """
    class Meta:
        model = Top_up_Payment
        fields = "__all__"



class SmsCallbackSerializers(serializers.ModelSerializer):
    """支付回调"""
    class Meta:
        model = SmsCallback
        fields = "__all__"

    def create(self, validated_data):

        return SmsCallback.objects.create(**validated_data)
