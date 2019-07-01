import hashlib
import json
from .serializables import PaySerializers, RechargeSerializers, SmsCallbackSerializers,PaymentSerializers
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView, CreateAPIView
from django.utils import timezone
import requests
import collections
import xmltodict
from rest_framework.response import Response
from rest_framework_jwt.authentication import jwt_decode_handler
from .models import RechargeModel,OrderInfo
from Users.models import EnterpriseCertificationInfo, Top_up_Payment
from Users.serializables import EnterpriseCertificationSerializer
#from up_down_chain.utils.send_template import Send_template
from up_down_chain.utils.send_template import Send_template
from oauth.models import OAuthWXUser
import xmltodict
from up_down_chain.utils.payment import get_pay_info,get_Recharge_pay_info
from oauth.models import CustomerInformation


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
            openid = request.query_params['openid']
            data_xml = data_str.decode()

            content = xmltodict.parse(data_xml)['xml']
            #print(content)
            data_dict = {
                "order_id": order_id,
                "mch_id": content['mch_id'],
                "result_code": content['result_code'],
                "openid": openid,
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
                Send_template().Payment_notice_Template(openid,content['total_fee'],order_id,access_token,content['time_end'])
                Send_template().CertificationNotice(openid, access_token)

                return HttpResponse("success")
            except Exception as e:
                return HttpResponse("success")
        except Exception as e:
            return HttpResponse("success")

class RechargePayment(GenericAPIView):

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
            openid = request.query_params['openid']
            data_xml = data_str.decode()

            content = xmltodict.parse(data_xml)['xml']

            data_dict = {
                "order_id": order_id,
                "mch_id": content['mch_id'],
                "result_code": content['result_code'],
                "openid": openid,
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
            
            if content['pay_result'] == '0':
                #print(1)
                try:
                    user = CustomerInformation.objects.get(username=openid)
                except Exception as e:
                    return Response({"token_state": False})
                try:
                    # 获取支付流水号
                    Recharge = RechargeModel.objects.get(mid=user.id, pay_order=order_id,pay_state=0)
                except Exception as e:
                    return Response({"find": False})
                # 流水号状态修改
                Recharge.pay_state = 1
                Recharge.save()
             
                total_fee = int(content["total_fee"]) / 100
                #print(total_fee)
                contents = EnterpriseCertificationInfo.objects.get(user=user.id)
               
                payment = Top_up_Payment.objects.get(userid=contents.company_id)
               
                payment.balance = float(payment.balance) + total_fee
                payment.save()
              
                access_token = get_redis_connection('wechatpy').get("access_token").decode()
              
                Send_template().SubscriptionPushTemplate(openid, total_fee,access_token,content['time_end'],user.id,payment.balance,user.first_name)
                Send_template().RefillAlertAdministrator(access_token,total_fee,user.id,user.first_name)
            print(10)
            return HttpResponse("success")
        except Exception as e:
            print(e)
            return HttpResponse("success")




class RechargeMent(GenericAPIView):

    serializer_class = RechargeSerializers
    queryset = RechargeModel.objects.all()

    def post(self,request):
        try:
            data_dict = request.data
            token = jwt_decode_handler(data_dict['token'])
            user = CustomerInformation.objects.get(username=token["username"])
        except Exception as e:
            return Response({"token_state":False})
        #if int(data_dict[total_fee]) < 101:
        #    return Response({"money":False})
        # 支付订单id
        order_id = timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)


        pay_info = get_Recharge_pay_info(user.username, user.id, order_id, data_dict['total_fee'])



        data = {
            "total_fee": data_dict['total_fee'],
            "pay_order": order_id,
            "mid":user.id
        }
        try:
            serializers = self.get_serializer(data=data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
        except Exception as e:
            return Response({"message":False})

        return Response({
            "pay_info": pay_info,
            "pay_order":serializers.data['pay_order']
        })

    # def put(self,request):
    #     try:
    #         data_dict = request.data
    #         token = jwt_decode_handler(data_dict['token'])
    #     except Exception as e:
    #         return Response({"token_state":False})
    #     try:
    #         Recharge = RechargeModel.objects.get(mid=token["user_id"],pay_order=data_dict['pay_order'],pay_state=0)
    #         pay_order = OrderInfo.objects.get(out_trade_no=data_dict['pay_order'],pay_result=0,openid=token['username'])
    #     except Exception as e:
    #         return Response({"find":False})
    #     Recharge.pay_state=1
    #     Recharge.save()
    #     total_fee = int(pay_order.total_fee) / 100
    #     content = EnterpriseCertificationInfo.objects.get(user=token['user_id'])
    #     try:
    #         payment = Top_up_Payment.objects.get(userid =content.company_id)
    #     except Exception as e:
    #         print(e)
    #     payment.balance=float(payment.balance)+total_fee
    #     #print(55)
    #     payment.save()
    #     #print(6)
    #     return Response({"mssage":True})

    def get(self,request):
        try:
            data_dict = request.query_params
            token = jwt_decode_handler(data_dict['token'])
        except Exception as e:
            return Response({"token_state":False})
        serializer = RechargeModel.objects.filter(mid=token['user_id'])
        return Response({
            "data":serializer
        })

class SmsCallbackView(CreateAPIView):
    """短信信息回调接口"""

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        data["batchId"] = str(data["batchId"])

        serializers = SmsCallbackSerializers(data=data, partial=True)

        if serializers.is_valid():
            serializers.save()

        else:
            return Response(serializers.errors)

        return Response({"message": "接收成功"})
