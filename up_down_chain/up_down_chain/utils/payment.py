import hashlib
import json
import collections
import random

import requests
import xmltodict
from django.utils import timezone


def get_pay_info(openid,user_id,order_id,total_fee):
    # MD5加密
    m = hashlib.md5()

    # 支付订单id
    pay_id = timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d'%user_id)

    data = collections.OrderedDict()
    data['body'] = 'Authentication'
    data['is_raw'] = '1'
    data['mch_create_ip'] = '117.48.207.24'
    data['mch_id'] = '103580084665'
    data['nonce_str'] = '6666678458646'
    data['notify_url'] = 'http://www.shangxialian.net:8000/pay/?order_id='+order_id+'&openid='+openid
    data['out_trade_no'] = pay_id
    data['service'] = 'pay.weixin.jspay'
    data['sign_type'] = 'MD5'
    data['sub_openid'] = openid
    data['total_fee'] = total_fee
    data['version'] = '1.0'

    # 数据格式处理
    xml = '<xml>'
    string_content = ''
    for key, value in data.items():
        string_content += key + '=' + value + '&'
        xml += '<' + key + '>''<![CDATA[' + value + ']]></' + key + '>'

    string_content += 'key=' + '31768c8eaf2c790b25ab01bd2ccca5ed'


    b = string_content.encode(encoding='utf-8')
    m.update(b)
    xml += '<sign>''<![CDATA[' + m.hexdigest().upper() + ']]></sign></xml>'

    head = {"Content-Type": "text/xml; charset=UTF-8", 'Connection': 'close'}
    res = requests.post('https://pay.swiftpass.cn/pay/gateway',data=xml,headers=head)

    root_xml = xmltodict.parse(res.text)['xml']

    pay_info = json.loads(root_xml['pay_info'])

    return pay_info

