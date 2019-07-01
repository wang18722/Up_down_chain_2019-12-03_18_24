import hashlib
import re

import time
from datetime import datetime

from PIL import Image
from mutagen._util import get_size
from rest_framework import serializers


from Users.models import Top_up_Payment, Record, Template, ManualMessagePost, EnterpriseCertificationInfo, Order, \
    PayCertificationInfo
from oauth.models import CustomerInformation


class Top_upSerializer(serializers.ModelSerializer):
    """更新消费余额序列化器"""

    class Meta:
        model = Top_up_Payment
        fields = ("balance",)

    def update(self, instance, validated_data):
        """更新余额"""
        # print(instance)
        # print(111111111111)
        # print(validated_data)
        # 更新余额
        # print(validated_data['balance'])
        instance = instance[0]
        instance.balance = validated_data['balance']
        # save保存操作
        instance.save()
        return instance


class RecordSerializer(serializers.ModelSerializer):
    """记录序列化器表"""

    class Meta:
        model = Record
        fields = "__all__"

    def create(self, validated_data):
        # print(1111111111)
        record = Record.objects.create(**validated_data)
        return record


class GetTemplateSerializer(serializers.ModelSerializer):
    '''获取模板序列化器'''
    class Meta:
        model = Template
        fields = ("id","template_name","sms_type","data_time","content","state")


class TemplateSerializer(serializers.ModelSerializer):
    """模板序列化器"""
    class Meta:
        model = Template
        fields = "__all__"
    def validate(self, attrs):
        if len(attrs["content"]) > 500:
            raise serializers.ValidationError("内容过多")
        return attrs

class ManualMessagePostSerializer(serializers.ModelSerializer):
    """手动营销"""

    class Meta:
        model =  ManualMessagePost


class EnterpriseCertificationSerializer(serializers.ModelSerializer):
    """企业认证序列化器"""
    #显示指明模型类没有的字段
    class Meta:
        model = EnterpriseCertificationInfo
        fields = '__all__'

    #验证手机号格式
    def validate_phone(self, attrs):
        """验证手机号或电话号码"""
        if not re.match(r"^1[3-9]\d{9}",attrs):
            raise serializers.ValidationError("手机号格式不正确")
        return attrs

    def create(self, validated_data):
        print(validated_data)
        obj = EnterpriseCertificationInfo.objects.create(**validated_data)

        return obj




class SaveOrderSerializer(serializers.ModelSerializer):
    """订单数据序列化器"""
    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        # print(validated_data)
        obj = Order.objects.create(**validated_data)
        return obj

class SaveConsumptionSerializer(serializers.ModelSerializer):
    """保存消费记录"""


class MoenyUpdateSerializer(serializers.ModelSerializer):
    """更新余额"""
    class Meta:
        model = Top_up_Payment
        fields = ("balance",)


    def update(self, instance, validated_data):
        instance.balance = validated_data["balance"]
        instance.save()
        return instance


class UpdateTemplateSerializer(serializers.ModelSerializer):
    """更新模板状态"""
    class Meta:
        model = Template
        fields = ("reviewer_name","state","reviewer_time")

    def update(self, instance, validated_data):

        instance.state = validated_data["state"]
        instance.reviewer_name = validated_data["reviewer_name"]
        instance.reviewer_time = datetime.now()
        instance.save()
        return instance

class AuthenticationAuditTemplateSerializer(serializers.ModelSerializer):
    """更新认证模板状态"""
    class Meta:
        model = EnterpriseCertificationInfo
        fields = ("reviewer_name","identity_status","reviewer_time","opinion")

    def update(self, instance, validated_data):

        instance.identity_status = validated_data["identity_status"]
        instance.reviewer_name = validated_data["reviewer_name"]
        instance.opinion = validated_data["opinion"]
        instance.reviewer_time = datetime.now()
        instance.save()
        return instance

class PayCertificationSerializer(serializers.ModelSerializer):
    """认证"""
    class Meta:
        model = PayCertificationInfo
        fields = "__all__"

   
    def create(self, validated_data):

        return PayCertificationInfo.objects.create(**validated_data)

class CreatePurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Top_up_Payment
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)

        return Top_up_Payment.objects.create(**validated_data)

class ObtainAuthenticationAuditTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseCertificationInfo
        fields = "__all__"


class  PayCertificationInfoSerializer(serializers.ModelSerializer):
    """订单记录更新"""
    class Meta:
        model = PayCertificationInfo
        fields = ("company_name",)

    def update(self, instance, validated_data):
        instance.company_name=validated_data["company_name"]

        instance.save()
        return instance

