from django.conf import settings
from rest_framework import serializers

from .models import Wxpay, Wxorder


class BaseSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, read_only=True)
    updated_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = None


class WxpaySerializer(BaseSerializer):
    """
        微信支付序列化类
    """

    class Meta:
        model = Wxorder

        fields = "__all__"
