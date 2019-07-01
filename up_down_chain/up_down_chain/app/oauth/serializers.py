from django.conf import settings
from rest_framework import serializers

from .models import Wxpay, OAuthWXUser,CustomerInformation


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
        model = Wxpay
        fields = "__all__"





class WXAuthUserSerializer(serializers.Serializer):
    """用户判定序列化器，使用JWT"""
    openid = serializers.CharField(label="openid", max_length=64)
    unionid = serializers.CharField(label="unionid", max_length=64)
    headimgurl = serializers.CharField(label="headimgurl")
    sex = serializers.CharField(label="sex")
    province = serializers.CharField(label="province")
    country = serializers.CharField(label="country")
    nickname = serializers.CharField(label="nickname")
    city = serializers.CharField(label="city")


    def create(self, validated_data):
        #print(validated_data["province"])
        # name = open(validated_data["nickname"],'wb',encoding="utf8")
        # print(validated_data["nickname"])
        user = CustomerInformation.objects.create(
            username=validated_data["openid"],
            first_name=validated_data["nickname"],
            city=validated_data["city"],
            headimgUrl=validated_data["headimgurl"],
            sex=validated_data["sex"],
            province=validated_data["province"],
            country=validated_data["country"],
        )
        user.set_password(validated_data["unionid"])

        oauth_wx = OAuthWXUser.objects.create(
            openid=validated_data["openid"],
            user=user,

        )
        oauth_wx.save()
        user.save()

        return oauth_wx


# from rest_framework import serializers
# from rest_framework.settings import api_settings
#
# from Users.models import User
# from oauth.utils import check_save_user_openid
# from .models import OAuthWXUser
#
#
# class OAuthWXUserSerializer(serializers.ModelSerializer):
#     """
#     保存微信用户序列化器
#     """
#     access_token = serializers.CharField(label='操作凭证', write_only=True)
#     token = serializers.CharField(read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('mobile', 'Contacts',  'access_token', 'Customer_id', 'username', 'token')
#         extra_kwargs = {
#             'Contacts': {
#                 'read_only': True
#             },
#             'username': {
#                 'read_only': True
#             },
#             'mobile': {
#                 'read_only': True,
#             }
#         }
#
#     def validate(self, attrs):
#         # 检验access_token
#         global Contacts
#         access_token = attrs['access_token']
#
#         openid = check_save_user_openid(access_token)
#         if not openid:
#             raise serializers.ValidationError('无效的access_token')
#
#         attrs['openid'] = openid
#         mobile = attrs['mobile']
#         # 如果联系人存在，检查用户手机号码
#         try:
#             user = User.objects.get(mobile=mobile)
#         except User.DoesNotExist:
#             pass
#
#         else:
#             attrs['Contacts'] = user
#         return attrs
#
#     def create(self, validated_data):
#         openid = validated_data['openid']
#         user = validated_data.get('user')
#         mobile = validated_data['mobile']
#         Contacts = validated_data['Contacts']
#
#         if not user:
#             # 如果用户不存在，创建用户，绑定openid（创建了OAuthWXUser数据）
#             user = User.objects.create_user(username=mobile, mobile=mobile, Contacts=Contacts)
#
#         OAuthWXUser.objects.create(username=user, openid=openid)
#
#         # 签发jwt token
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#
#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#
#         user.token = token
#
#         return user
