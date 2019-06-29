from django.conf import settings
import requests

from Users.models import PayCertificationInfo
from oauth.models import CustomerInformation
import json
import datetime
class Send_template(object):
    def Payment_notice_Template(self, openid, total_fee, order_id, access_token, time):
        # access_token = WeChatClient(appid=settings.WXAPPID, secret=settings.WXAPPSECRET).access_token
        """
        {【上下链】平台有新的企业申请认证，请尽快审核。}
        收款金额：{200.00元}
        商户名称：{企业名称}
        订单号：{订单编号}
        付款用户：{付款的微信昵称}
        订单时间：{2018-12-24 18:18}
        {今日累计****家企业申请认证。}

        """
        certificat = PayCertificationInfo.objects.get(order_id=order_id)
        user = CustomerInformation.objects.get(username=openid)
        for i in range(2):
            if i == 0:
                openids = "oO5Eq6Gii1YiUQ2r_PBdgq8swz3Q"
            else:
                openids = "oO5Eq6NGE1zV94yoHgLZnhcAJNOc"
            total_fee = int(total_fee)/100
            data = {
                "touser": openids,
                "url": "http://www.shangxialian.net/js/#/company-cert",
                "template_id": settings.TEMPLATE_DICT["2"],
                "data": {
                    "first": {
                        "value": "【上下链】平台有新的企业申请认证，请尽快审核。"
                    },
                    "keyword1": {
                        "value": str(total_fee) + "元",
                        "color": "#09a3a3"
                    },
                    "keyword2": {
                        "value": certificat.company_name,
                        "color": "#09a3a3"
                    },
                    "keyword3": {
                        "value": order_id,
                        "color": "#09a3a3"
                    },
                    "keyword4": {
                        "value": user.first_name,
                        "color": "#09a3a3"
                    },
                    "keyword5": {
                        "value": time[0:4]+'-'+time[4:6]+'-'+time[6:8]+' '+time[8:10]+':'+time[10:12],
                        "color": "#09a3a3"
                    },
                    "remark": {
                        "value": "",
                    }
                }
            }
            i += 1
            requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                          data=json.dumps(data))

    def Authentication_adopt(self,access_token, company_name, user_id,state):
        user = CustomerInformation.objects.get(id=user_id)
        if state == 2:
            state = "通过"
        else:
            state = "不通过"
        data = {
            "touser": user.username,
            "url": "http://www.shangxialian.net/",
            "template_id": settings.TEMPLATE_DICT["7"],
            "data": {
                "first": {
                    "value": "【上下链】尊敬的" + user.first_name + "," + company_name + "企业会员已审核"+state +"。",

                },
                "keyword1": {
                    "value": company_name,
                },
                "keyword2": {
                    "value": str(datetime.datetime.today())[:19],
                },
                "remark": {
                    "value": "用上下链触客  AI赋能营销",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                      data=json.dumps(data))
    def To_examine_template(self,id,content,access_token):
        """
        短信模板审核通知
        :param id:
        :param content:
        :return:
        """
        # access_token = WeChatClient(appid=settings.WXAPPID, secret=settings.WXAPPSECRET).access_token

        user = CustomerInformation.objects.get(id=id)


        for i in range(2):
            if i == 0:
                openid = "oO5Eq6Gii1YiUQ2r_PBdgq8swz3Q"
            else:
                openid = "oO5Eq6NGE1zV94yoHgLZnhcAJNOc"
            data = {
                "touser": openid,
                "url":"http://www.shangxialian.net/js/#/operator",
                "template_id": settings.TEMPLATE_DICT["15"],
                "data": {
                    "first": {
                        "value": "【上下连】"+user.first_name + "：" + "已提交短信模板资料，请尽快审核！",
                       
                    },
                    "keyword1": {
                        "value": content,
                        "color": "#09a3a3"
                    },
                    "keyword2": {
                        "value": str(datetime.datetime.today())[:19],
                        "color": "#09a3a3"
                    },
                    "remark": {
                        "value": "请点击审核！",
                    }
                }
            }
            i +=1
            requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token='+access_token, data=json.dumps(data))


    def To_examine_template_result(self,token,state,access_token):
        """
        审核结果通知
        :param token:
        :param state:
        :return:
        """
        user = CustomerInformation.objects.get(id=token['user_id'])
        # access_token = WeChatClient(appid=settings.WXAPPID, secret=settings.WXAPPSECRET).access_token
        if state == 2:
            state = "通过"
        else:
            state = "不通过"
        data = {
            "touser": user.username,
            "url": "http://www.shangxialian.net/",
            "template_id": settings.TEMPLATE_DICT["17"],
            "data": {
                "first": {
                    "value": "【上下链】尊敬的"+user.first_name + "用户，您上传的短信模板内容审核结果已出.",

                },
                "keyword1": {
                    "value": state,
                },
                "keyword2": {
                    "value": str(datetime.datetime.today())[:19],
                },
                "remark": {
                    "value": "现在您可以进行短信触客推送",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token='+access_token, data=json.dumps(data))

    def To_Examine_Template_Subscribe(self,user,keywords_array,area_name,access_token):
        # access_token = WeChatClient(appid=settings.WXAPPID, secret=settings.WXAPPSECRET).access_token

        data = {
            "touser": user.username,
            "url": "http://www.shangxialian.net/",
            "template_id": settings.TEMPLATE_DICT["1"],
            "data": {
                "first": {
                    "value": "【上下链】"+ user.first_name + ",您订阅推送关键词内容设置成功。每日为您‘订阅推送’最新采招商机及微信提醒通知服务",

                },
                "keyword1": {
                    "value": str(datetime.datetime.today())[:19],
                },
                "keyword2": {
                    "value": "每日提醒",
                },
                "keyword3": {
                    "value": keywords_array,
                },
                "keyword4": {
                    "value": area_name,
                },
                "remark": {
                    "value": "用上下链触客  AI赋能营销",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,data=json.dumps(data))
    def Notification_fail_Template(self, access_token,company_name,user_id):
        user = CustomerInformation.objects.get(id=user_id)

        data = {
            "touser": user.username,
            "url": "http://www.shangxialian.net/",
            "template_id": settings.TEMPLATE_DICT["8"],
            "data": {
                "first": {
                    "value": "【上下链】" + user.first_name + "您好,您申请加入的上下连认证企业"+company_name+",企业管理员未能通过您的申请.请与企业管理人员联系确认后在重新申请加入.",

                },
                "keyword1": {
                    "value": str(datetime.datetime.today())[:19],
                    "color": "#09a3a3"
                },
                "keyword2": {
                    "value": "不通过",
                    "color": "#09a3a3"
                },
                "keyword3": {
                    "value": "资料审核失败",
                    "color": "#09a3a3"
                },
                "remark": {
                    "value": "用上下链触客  AI赋能营销",
                }
            }
        }
        requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,data=json.dumps(data))

    def SubscriptionPushTemplate(self,access_token):
        pass