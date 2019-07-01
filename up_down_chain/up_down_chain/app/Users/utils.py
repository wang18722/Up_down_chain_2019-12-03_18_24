
import os

#处理图片代码封装
from datetime import datetime
from random import random

from mutagen._util import get_size
from PIL import Image

from Users.serializables import CreatePurseSerializer, PayCertificationSerializer, EnterpriseCertificationSerializer, \
    PayCertificationInfoSerializer
from up_down_chain.utils.payment import get_pay_info

"""图片压缩代码封装"""
def imag(company_name,image):
    # 获取图片大小
    o_size = get_size(image)
    quality = 80
    step = 10
    # 处理图片名称
    data_time = datetime.now().strftime("%Y%m%d%H%M%S")
    image_name = data_time + company_name + "." + image.name.split(".")[-1]

    # 图片路径
    # path = "/root/Up_down_chain/up_down_chain/static/" + image_name
    path = "/root/Up_down_chain/up_down_chain/static/" + image_name

    if o_size <= 40000:
        im = Image.open(image)
        im.save(path, quality=quality)
        return image_name

    # path=""
    # 图片压缩
    while o_size > 400000:
        im = Image.open(image)
        im.save(path, quality=quality)

        if quality - step < 0:
            break
        quality -= step
        o_size = os.path.getsize(path)
    return image_name


"""数据处理并封装"""
class Serializers_obj(object):

    def createpurse(self,wallet):
        """调起支付接口保存"""
        ser = CreatePurseSerializer(data=wallet, partial=True)

        if ser.is_valid():
            ser.save()


    def pay(self,data_info):
        """支付保存"""
        serializer = PayCertificationSerializer(data=data_info, partial=True)

        if serializer.is_valid():
            serializer.save()


    def enterprise(self,data):
        """认证企业保存"""
        serializer = EnterpriseCertificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()


    def recordupdate(self,obj,data):
        """订单记录更新"""
        serializer = PayCertificationInfoSerializer(obj,data=data)
        if serializer.is_valid():
            serializer.save()








