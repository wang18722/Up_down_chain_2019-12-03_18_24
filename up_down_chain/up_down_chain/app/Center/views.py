from django.shortcuts import render

# Create your views here.
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler

from Center.serializers import SelfPortraitSerializers
from Users.models import EnterpriseCertificationInfo, Top_up_Payment, Order


class UserCenterView(RetrieveAPIView):
    """个人中心"""

    def get(self, request, *args, **kwargs):
        try:
            token = jwt_decode_handler(request.GET["token"])
        except Exception as e:
            return Response({"token_state":False})
        try:
            obj = EnterpriseCertificationInfo.objects.filter(user=token["user_id"], identity_status=2).first()
        except:
            return Response({"message": "查询出错"})

        if obj:
            try:
                # 查询余额
                T_obj = Top_up_Payment.objects.filter(userid=obj.company_id).first()
                # 查询订单消费
                order_obj = Order.objects.filter(company_id=obj.company_id).filter()
            except:
                return Response({"message": "查询出错"})
            # 计算总金额
            money = 0
            for i in order_obj:
                money += i.total_amount
            data = {
                "recommended_count": obj.recommended,
                "access_count": obj.access,
                "consumption_count": money,
                "balance": T_obj.balance,
                'focus': 0,
                "status":obj.identity_status,
                "company_name":obj.name,
            }

            return Response(data)

        data = {
            "recommended_count": 0,
            "access_count": 0,
            "consumption_count": 0,
            "balance": 0,
            'focus': 0,
            "status":3
        }

        return Response(data)


class SelfPortraitView(ListCreateAPIView):
    """自画像"""

    def get(self, request, *args, **kwargs):
        try:
            token = jwt_decode_handler(request.GET["token"])
        except Exception as e:
            return Response({"token_state":False})
        try:
            obj = EnterpriseCertificationInfo.objects.filter(user=token["user_id"], identity_status=2).first()
        except:
            return Response({"message": "查询出错"})
        if not obj:
            return Response({"message":"error"})
        data = {
            "kind": obj.kind,
            "lndividual_labels": obj.lndividual_labels
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            token = jwt_decode_handler(data["token"])
        except:
            return Response({"token_state": False})
        try:
            obj = EnterpriseCertificationInfo.objects.filter(user=token["user_id"], identity_status=2).first()
        except:
            return Response({"message": "查询出错"})
        if not obj:
            return Response({"message":"error"})

        data["kind"] = data["kind"]
        data["lndividual_labels"] = data["lndividual_labels"]
        serializers = SelfPortraitSerializers(obj, data=data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response({"message": "保存成功"})
        else:
            return Response(serializers.errors)
