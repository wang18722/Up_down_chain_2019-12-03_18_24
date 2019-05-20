import hashlib
import random
import time
from urllib import parse
from xml.etree.ElementTree import fromstring
import requests
# 导入配置文件
from django.conf import settings



class WechatAPI(object):
    """微信API接口"""

    def __init__(self):
        self.config = settings  # 配置文件
        self._access_token = None  # 默认token为空
        self._openid = None  # 默认openid为空
        self.dic = {}  # 定义空字典存放键值对

    @staticmethod
    def process_response_login(rsp):
        """解析微信登录返回的json数据，返回相对应的dict, 错误信息"""
        # 判断获取到的状态码不等于200则返回NOne值和一个字典
        if 200 != rsp.status_code:
            return None, {'code': rsp.status_code, 'msg': 'http error'}
        try:
            # 获取json的内容
            content = rsp.json()

        except Exception as e:
            return None, {'code': 9999, 'msg': e}
        # 判断如果errcode在json内容里面 并且 errcode的参数不等于0,返回空值个errcode对应的参数
        if 'errcode' in content and content['errcode'] != 0:
            return None, {'code': content['errcode'], 'msg': content['errmsg']}

        # 返回内容一个字典
        return content, None

    def process_response_pay(self, rsp):
        """解析微信支付下单返回的json数据，返回相对应的dict, 错误信息"""
        # 调用xml转数组格式,传入响应
        rsp = self.xml_to_array(rsp)
        # 判断响应中的return_code 不等于success,也就是没有响应成功则返回信息
        if 'SUCCESS' != rsp['return_code']:
            return None, {'code': '9999', 'msg': rsp['return_msg']}
        # 判断支付id不在响应中则返回错误或空值
        if 'prepay_id' in rsp:
            return {'prepay_id': rsp['prepay_id']}, None
        # 返回响应
        return rsp, None

    @staticmethod
    def create_time_stamp():
        """产生时间戳"""
        now = time.time()
        return int(now)

    @staticmethod
    def create_nonce_str(length=32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"

        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        # 拼接字符串并返回
        return "".join(strs)

    @staticmethod
    def xml_to_array(xml):
        """将xml转为array"""
        array_data = {}
        root = fromstring(xml)
        print(root)
        for child in root:
            value = child.text
            array_data[child.tag] = value

        # 返回一个字典{child.tag:value}
        return array_data

    def get_sign(self):
        """生成签名"""
        # 签名步骤一：按字典序排序参数
        key = sorted(self.dic.keys())
        buffer = []
        for k in key:
            buffer.append("{0}={1}".format(k, self.dic[k]))
        # self.dic["paySign"] = self.get_sign(jsApiObj)

        parm = "&".join(buffer)
        # 签名步骤二：在string后加入KEY
        parm = "{0}&key={1}".format(parm, self.config.API_KEY).encode('utf-8')
        # 签名步骤三：MD5加密
        signature = hashlib.md5(parm).hexdigest()
        # 签名步骤四：所有字符转为大写
        result_ = signature.upper()
        print(result_)
        return result_

    def array_to_xml(self, sign_name=None):
        """array转xml"""
        if sign_name is not None:
            self.dic[sign_name] = self.get_sign()
        xml = ["<xml>"]
        for k in self.dic.keys():
            xml.append("<{0}>{1}</{0}>".format(k, self.dic[k]))
        xml.append("</xml>")
        return "".join(xml)


class WechatLogin(WechatAPI):
    """微信登录"""

    def get_code_url(self):
        """微信内置浏览器获取网页授权code的url"""
        # 完整的数据:https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx841a97238d9e17b2&redirect_uri=http://cps.dianping.com/weiXinRedirect&response_type=code&scope=snsapi_userinfo&state=type%3Dquan%2Curl%3Dhttp%3A%2F%2Fmm.dianping.com%2Fweixin%2Faccount%2Fhome
        url = self.config.defaults.get('wechat_browser_code') + (
            '?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' %
            (self.config.APPID, parse.quote(self.config.REDIRECT_URI),
             self.config.SCOPE, self.config.STATE if self.config.STATE else ''))
        print(url)

        return url

    def get_code_url_pc(self):
        """pc浏览器获取网页授权code的url"""
        url = self.config.defaults.get('pc_QR_code') + (
            '?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' %
            (self.config.APPID, parse.quote(self.config.REDIRECT_URI), self.config.PC_LOGIN_SCOPE,
             self.config.STATE if self.config.STATE else ''))
        return url

    def get_access_token(self, code):
        """获取access_token"""
        params = {
            # 公众号id
            'appid': self.config.APPID,
            # 公证号授权证书
            'secret': self.config.APPSECRET,
            # 用户同意授权,获取的code
            'code': code,

            'grant_type': 'authorization_code'
        }
        # 调用微信登录返回的json数据函数传一个响应进去
        # 传回去的数据:https://api.weixin.qq.com/sns/oauth2/access_token和参数一个字典
        token, err = self.process_response_login(requests.get(self.config.defaults.get('wechat_browser_access_token'),
                                                              params=params))

        # 判断如果err为空,一开始的空token等于登录用户的token,openid也是并返回
        if not err:
            self._access_token = token['access_token']
            self._openid = token['openid']
        return self._access_token, self._openid

    def get_user_info(self, access_token, openid):
        """获取用户信息"""
        params = {
            'access_token': access_token,
            'openid': openid,
            'lang': self.config.LANG
        }

        # 获取微信内置浏览器获取用户信息接口并返回
        return self.process_response_login(requests
                                           .get(self.config.defaults.get('wechat_browser_user_info'), params=params))


class WechatTemplates(WechatAPI):
    def __init__(self):
        super().__init__()
        self.mp_access_token = None
        self.mp_expires_in = None

    def get_mp_access_token(self):
        """获取公众号的access_token"""
        # err_code = {
        #     '-1': '系统繁忙，请稍候再试',
        #     '0': '请求成功',
        #     '40001': 'AppSecret错误或者AppSecret不属于这个公众号，请开发者确认AppSecret的正确性',
        #     '40002': '请确保grant_type字段值为client_credential',
        #     '40164': '调用接口的IP地址不在白名单中，请在接口IP白名单中进行设置',
        # }
        # 获取微信公众号的参数
        url = self.config.defaults.get('mp_access_token') + (
            '?grant_type=%s&appid=%s&secret=%s' %
            (self.config.GRANT_TYPE, self.config.APPID,
             self.config.APPSECRET))
        print(url + "1111111111111")
        # eval的作用返回传入字符串的表达式的结果
        token_data = eval(requests.get(url).content)
        # 判断 token如果不在token_data
        if 'access_token' not in token_data:
            return token_data['errcode'], token_data['errmsg'], False
        else:
            self.mp_access_token = token_data['access_token']
            self.mp_expires_in = token_data['expires_in']
            # 返回用户存在
            return self.mp_access_token, self.mp_expires_in, True

    # 以下功能暂不使用
    # def change_industry(self):
    #     """设置所属行业，每月可修改行业1次"""
    #     url = self.config.defaults.get('change_industry') + (
    #         '?access_token=%s' % self.mp_access_token)
    #     prams = {
    #         "industry_id1": "23",
    #         "industry_id2": "31"
    #     }
    #     data = requests.post(url, prams)
    #
    # def get_industry(self):
    #     """获取行业信息"""
    #     if self.mp_access_token is None:
    #         _, msg, success = self.get_mp_access_token()
    #         if not success:
    #             return msg, False
    #     url = self.config.defaults.get('get_industry') + (
    #         '?access_token=%s' % self.mp_access_token)
    #     industry_data = requests.get(url)
    #     if 'primary_industry' in industry_data:
    #         primary_industry = industry_data['primary_industry']
    #         secondary_industry = industry_data['secondary_industry']
    #         return primary_industry, secondary_industry, True
    #     else:
    #         return '', '获取行业信息错误', False
    #
    # def get_templates_id(self):
    #     pass
    #

    def send_templates_message(self, touser, template_id, data, url=None, miniprogram=None):
        """发送模板消息"""

        post_data = {
            "touser": touser,
            "template_id": template_id,
            "data": data
        }
        if url is not None:
            post_data['url'] = url
        if miniprogram is not None:
            post_data['miniprogram'] = miniprogram
        url = self.config.defaults.get('send_templates_message') + (
            '?access_token=%s' % self.mp_access_token)
        back_data = requests.post(url, json=post_data)
        print(back_data+"===================================")
        if "errcode" in back_data and back_data["errcode"] == 0:
            return True
        else:
            return False


class WechatPayAPI(WechatAPI):
    """微信支付API"""
    def __init__(self, package, sign_type=None):
        super().__init__()
        # 公众号id
        self.appId = self.config.APPID
        # 时间戳
        self.timeStamp = self.create_time_stamp()
        # 产生随机字符串
        self.nonceStr = self.create_nonce_str()
        # 包
        self.package = package
        # 对象类型
        self.signType = sign_type
        # 一个有数据的字典
        self.dic = {"appId": self.appId, "timeStamp": "{0}".format(self.create_time_stamp()),
                    "nonceStr": self.create_nonce_str(), "package": "prepay_id={0}".format(self.package)}
        if sign_type is not None:
            self.dic["signType"] = sign_type
        else:
            self.dic["signType"] = "MD5"

    def get_dic(self):
        self.dic['paySign'] = self.get_sign()
        return self.dic


class WechatOrder(WechatAPI):
    """微信订单"""
    def __init__(self, body, trade_type, out_trade_no, total_fee, spbill_create_ip, notify_url, device_info=None,
                 sign_type=None, attach=None, fee_type=None, time_start=None, time_expire=None, goods_tag=None,
                 product_id=None, detail=None, limit_pay=None, openid=None, scene_info=None):
        super().__init__()
        self.device_info = device_info  #
        self.nonce_str = self.create_nonce_str()
        self.sign_type = sign_type  #
        self.detail = detail  #
        self.body = body
        self.attach = attach  #
        self.out_trade_no = out_trade_no
        self.fee_type = fee_type  #
        self.total_fee = total_fee
        self.spbill_create_ip = spbill_create_ip
        self.time_start = time_start  #
        self.time_expire = time_expire  #
        self.goods_tag = goods_tag  #
        self.notify_url = notify_url
        self.trade_type = trade_type
        self.product_id = product_id  #
        self.limit_pay = limit_pay  #
        self.openid = openid  #
        self.scene_info = scene_info  #
        self.dic = {"appid": self.config.APPID, "mch_id": self.config.MCH_ID,
                    "nonce_str": self.nonce_str, "body": self.body,
                    'out_trade_no': out_trade_no,
                    'openid': self.openid,
                    "total_fee": self.total_fee, "spbill_create_ip": self.spbill_create_ip,
                    "notify_url": self.notify_url,
                    "trade_type": self.trade_type}
        if self.device_info is not None:
            self.dic["device_info"] = self.device_info
        if self.sign_type is not None:
            self.dic["sign_type"] = self.sign_type
        if self.detail is not None:
            self.dic["detail"] = self.detail
        if self.attach is not None:
            self.dic["attach"] = self.attach
        if self.fee_type is not None:
            self.dic["fee_type"] = self.fee_type
        if self.time_start is not None:
            self.dic["time_start"] = self.time_start
        if self.time_expire is not None:
            self.dic["time_expire"] = self.time_expire
        if self.goods_tag is not None:
            self.dic["goods_tag"] = self.goods_tag
        if self.product_id is not None:
            self.dic["product_id"] = self.product_id
        if self.limit_pay is not None:
            self.dic["limit_pay"] = self.limit_pay
        if self.openid is not None:
            self.dic["openid"] = self.openid
        if self.scene_info is not None:
            self.dic["scene_info"] = self.scene_info

    def order_post(self):
        """订单请求"""
        if self.config.APPID is None:
            return None, True
        xml_ = self.array_to_xml('sign')
        data = requests.post(self.config.defaults['order_url'], data=xml_.encode('utf-8'),
                             headers={'Content-Type': 'text/xml'})
        return self.process_response_pay(data.content)
