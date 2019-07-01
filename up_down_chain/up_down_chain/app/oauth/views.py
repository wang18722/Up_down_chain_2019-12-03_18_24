from django.contrib.auth import authenticate, login

from oauth.models import OAuthWXUser, CustomerInformation
from oauth.serializers import WXAuthUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from wechatpy import WeChatOAuth
from django.conf import settings

class UserOuthsUrl(APIView):
    """
    微信授权
    """

    def get(self, request):

        # 微信授权配置
        OauthWX =WeChatOAuth(app_id=settings.WXAPPID,secret=settings.WXAPPSECRET,redirect_uri=settings.REDIRECT_URI,scope=settings.SCOPE,state='/')

        # 微信授权url
        auth_url = OauthWX.authorize_url

        # pc_auth_url = OauthWX.qrconnect_url
        return Response({
            'auth_url':auth_url
        })


class UserOpenIdViews(APIView):
    """
    微信用户保存
    """
    # serializer_class = WXAuthUserSerializer

    def get(self,request):

        # 登陆成功后code
        code = request.query_params.get('code')

        if not code:
            print(1)
            return Response({'message':'缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        # 微信授权配置
        OauthQQ = WeChatOAuth(app_id=settings.WXAPPID, secret=settings.WXAPPSECRET,redirect_uri=settings.REDIRECT_URI, scope=settings.SCOPE, state='/')

        try:
            OauthQQ.fetch_access_token(code)

            # 用户信息
            wx_user_content = OauthQQ.get_user_info()

        except Exception:
            return Response({'message': '微信服务器异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 判断用户是否绑定缘道美
        try:
            OAuthWXUser.objects.get(openid=wx_user_content['openid'])
        except Exception as e:
            if len(wx_user_content['province']) == 0:
                wx_user_content['province'] = "0"
            if len(wx_user_content['city']) == 0:
                wx_user_content['city'] = "0"
            print(wx_user_content)
            # 获取序列化器,校验数据
            try:
                serializer = WXAuthUserSerializer(data=wx_user_content)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as e:
                print(e)
            # 加密openid返回token
            # access_token_openid = generate_save_token(wx_user_content['openid'])
            # return Response({'access_token': access_token_openid})
            # oauth_user_wx = OAuthWXUser.objects.get(openid=wx_user_content['openid'])

        # 如果用户微信已经绑定缘道美，直接生成JWT token，并返回
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = authenticate(username=wx_user_content['openid'], password=wx_user_content["unionid"])

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        login(request, user)
        # 暂时返回token..具体看需求
        response = Response({
            'token': token,
            'user_id': user.id,
            'username': user.first_name,
            'headimgUrl':user.headimgUrl
        })

        return response




