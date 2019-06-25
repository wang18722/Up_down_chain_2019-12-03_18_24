import hashlib
import json

from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from django.utils import timezone
import requests
import collections
import xmltodict
from rest_framework.response import Response
from rest_framework_jwt.authentication import jwt_decode_handler

from Users.models import EnterpriseCertificationInfo
from Users.serializables import EnterpriseCertificationSerializer
from up_down_chain.utils.send_template import Send_template
from .serializables import PaySerializers
from oauth.models import OAuthWXUser
import xmltodict



class PufaPayment(GenericAPIView):

    serializer_class = PaySerializers

    def post(self,request):
        """
        支付订单保存
        :param request:
        :return:
        """
        try:
            data_str = request.body

            order_id = request.query_params['order_id']

            data_xml = data_str.decode()

            content = xmltodict.parse(data_xml)['xml']

            data_dict = {
                "order_id": order_id,
                "mch_id": content['mch_id'],
                "result_code": content['result_code'],
                "openid": content['openid'],
                "trade_type": content['trade_type'],
                "is_subscribe": content['is_subscribe'],
                "pay_result": content["pay_result"],
                "transaction_id": content['transaction_id'],
                "out_transaction_id": content['out_transaction_id'],
                "time_end": content['time_end'],
                "total_fee": content["total_fee"],
                "bank_type": content['bank_type'],
                "out_trade_no": content['out_trade_no']
            }

            serializers = self.get_serializer(data=data_dict)
            serializers.is_valid(raise_exception=True)
            serializers.save()

            try:
                access_token = get_redis_connection('wechatpy').get("access_token").decode()
                Send_template().Payment_notice_Template(content['openid'],content['total_fee'],order_id,access_token,content['time_end'])
                return HttpResponse("success")
            except Exception as e:
                return HttpResponse("success")
        except Exception as e:
            return HttpResponse("success")



    # def get(self,request):
    #
    #     token = jwt_decode_handler(request.query_params['token'])
    #
    #     try:
    #         user = OAuthWXUser.objects.get(user_id=token['user_id'])#
    #     except Exception:
    #         return Response({
    #             "massage":False
    #         })
    #     # 支付订单id
    #     pay_id = timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d'%user.id)
    #
    #     data = collections.OrderedDict()
    #     data['body'] = 'Authentication'
    #     data['is_raw'] = '1'
    #     data['mch_create_ip'] = '117.48.207.24'
    #     data['mch_id'] = '103580084665'
    #     data['nonce_str'] = pay_id
    #     data['notify_url'] = 'www.shangxialian.net:8000/pay/'
    #     data['out_trade_no'] = pay_id
    #     data['service'] = 'pay.weixin.jspay'
    #     data['sign_type'] = 'MD5'
    #     data['sub_openid'] = user.openid
    #     data['total_fee'] = '1'
    #     data['version'] = '1.0'
    #
    #     # 数据格式处理
    #     xml = '<xml>'
    #     string_content = ''
    #     for key, value in data.items():
    #         string_content += key + '=' + value + '&'
    #         xml += '<' + key + '>''<![CDATA[' + value + ']]></' + key + '>'
    #
    #     string_content += 'key=' + '31768c8eaf2c790b25ab01bd2ccca5ed'
    #
    #     # MD5加密
    #     m = hashlib.md5()
    #     b = string_content.encode(encoding='utf-8')
    #     m.update(b)
    #     xml += '<sign>''<![CDATA[' + m.hexdigest().upper() + ']]></sign></xml>'
    #
    #     head = {"Content-Type": "text/xml; charset=UTF-8", 'Connection': 'close'}
    #     res = requests.post('https://pay.swiftpass.cn/pay/gateway',data=xml,headers=head)
    #
    #     root_xml = xmltodict.parse(res.text)['xml']
    #
    #     pay_info = json.loads(root_xml['pay_info'])
    #
    #     # # 订单生成
    #     # data_dict = {
    #     #     "user":user.user.id,
    #     #     "order_id": pay_id,
    #     #     "sub_openid": user.openid,
    #     #     "total_amount": int(data['total_fee'])/100,
    #     # }
    #     #
    #     # serializer = self.get_serializer(data=data_dict)
    #     # serializer.is_valid(raise_exception=True)
    #     # serializer.save()
    #
    #     return Response(pay_info)