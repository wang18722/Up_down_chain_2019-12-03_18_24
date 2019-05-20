from django.utils import timezone
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.urls import login
from rest_framework.utils import json
from rest_framework.views import APIView

from subscribe.models import User
from utils.to_xml import toXML
from .models import Wxorder
from .utils import WechatLogin, WechatPayAPI, WechatOrder


class WechatViewSet(APIView):
    wechat_api = WechatLogin()


class AuthView(WechatViewSet):
    """身份验证视图"""
    def get(self, request):
        url = self.wechat_api.get_code_url()
        return redirect(url)


class GetInfoView(WechatViewSet):
    """获取信息视图"""
    def get(self, request):
        print(request.GET.get("code"))
        if 'code' in request.GET:
            code = request.GET['code']
            token, openid = self.wechat_api.get_access_token(code)
            if token is None or openid is None:
                return HttpResponseServerError('get code error')
            user_info, error = self.wechat_api.get_user_info(token, openid)
            if error:
                return HttpResponseServerError('get access_token error')
            user_data = {
                'nickname': user_info['nickname'],
                'sex': user_info['sex'],
                'province': user_info['province'].encode('iso8859-1').decode('utf-8'),
                'city': user_info['city'].encode('iso8859-1').decode('utf-8'),
                'country': user_info['country'].encode('iso8859-1').decode('utf-8'),
                'avatar': user_info['headimgurl'],
                'openid': user_info['openid']
            }
            user = Wxorder.objects.filter(is_effective=True).filter(wechat=user_data['openid'])

            if user.count() == 0:
                user = Wxorder.objects.create(username=user_data['nickname'],
                                                  wechat_avatar=user_data['avatar'],
                                                  wechat=user_data['openid'],
                                                  password='')
                login(request, user)
            else:
                login(request, user.first())
            # 授权登录成功，进入主页
            # return home(request)

class WechatPay(APIView):
    """微信支付"""
    def post(self,request):
        # 这个if判断是我传入的订单的id，测试的时候没有传入，你可以测试的时候去掉这个判断

        if 'order' in request.body.decode():
            # order = request.POST['order']
            # order = Order.objects.filter(is_effective=True).filter(uuid=order).first()
            print(11111111111111111111)

            body = 'JSP支付测试'
            trade_type = 'JSAPI'
            import random
            rand = random.randint(0, 100)
            out_trade_no = 'HSTY3JMKFHGA325' + str(rand)
            total_fee = 1
            spbill_create_ip = '192.168.179.143'
            notify_url = 'http://sxl.weiren.me/sxl/success'
            print(request.session)
            order = WechatOrder(body=body,
                                trade_type=trade_type,
                                out_trade_no=out_trade_no,
                                openid=request.session['openid'],
                                total_fee=total_fee,
                                spbill_create_ip=spbill_create_ip,
                                notify_url=notify_url)
            datas, error = order.order_post()
            if error:

                return Response({'massig':'get access_token error'})
            order_data = datas['prepay_id'].encode('iso8859-1').decode('utf-8'),
            pay = WechatPayAPI(package=order_data[0])
            dic = pay.get_dic()

            dic["package"] = "prepay_id=" + order_data[0]
            return HttpResponse(json.dumps(dic), content_type="application/json")


def success(request):
    # 这里写支付结果的操作，重定向
    print("=============================================")
    return redirect('/')

class PayBaseInfo(APIView):

    def post(self,request):
        user = User.objects.get(id=1)

        dict_data = {
            'service' : 'pay.weixin.jspay',  # 接口类型
            'mch_id' : '7551000001',  # 商务号
            'is_raw' : '1',  # 原生js
            'is_minipg' : '0',  # 1为小程序支付
            'out_trade_no' : timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id),  # 订单号[非支付订单号]
            'body' : "task",  # 订单描述
            'sub_openid' : '12342',  # openid
            #'sub_appid' : 'wx7db18dc71a69a978',  # 公众号openid
            'total_fee' : '1000',
            'nonce_str' : 'k5gm7je6-h$i=hsn*1_n%b1(2r%p5$@x063',
            'mch_create_ip' : '192.168.179.143',
            'sign' : '9d101c97133837e13dde2d32a5054abb',
            'notify_url' : 'www.baidu.com',
        }
        import requests
        response = requests.post('https://pay.swiftpass.cn/pay/gateway',data=toXML(dict_data))
        print(response.content.decode())
        print(toXML(dict_data))