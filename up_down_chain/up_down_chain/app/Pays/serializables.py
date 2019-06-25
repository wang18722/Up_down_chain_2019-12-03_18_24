from rest_framework import serializers

from oauth.models import OAuthWXUser
from .models import OrderInfo
class PaySerializers(serializers.ModelSerializer):
    """
    支付序列化器
     """

    class Meta:
        model = OrderInfo
        fields = "__all__"
