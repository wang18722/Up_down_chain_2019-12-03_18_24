import hashlib
import urllib.request
import json


class REST(object):
    account = 's2204026'
    password = "abc123"
    headers = {'Content-Type': 'application/json'}
    requestld = ''
    url = "http://www.17int.cn/xxsmsweb/smsapi/batchSend.json"
    extno = ''

    def content(self, contents, mobile):
        """获取手机号,和发送内容"""
        bReqContents = [{'mobile': mobile, "content": contents + " 回T退订"}]
        return bReqContents

    def encryption(self, password):
        """MD5加密"""

        m = hashlib.md5()
        p = password.encode(encoding="utf_8")
        m.update(p)
        str_md5 = m.hexdigest()
        print(str_md5)

        return str_md5

    def run(self, mobile,data):
        print(data)
        """执行函数"""
        sms_dict = {}
        sms_dict["account"] = self.account
        sms_dict["password"] = self.encryption(self.password)
        sms_dict["bReqContents"] = self.content(data['contents'], mobile)
        sms_dict["requestld"] = data["username"]
        sms_dict["extno"] = self.extno
        # print(sms_dict)
        # print(self.url)
        # print(self.headers)
        # print(self.url)

        # 请求
        requests = urllib.request.Request(url=self.url, headers=self.headers, data=json.dumps(sms_dict).encode())
        # print(requests)
        # 响应
        response = urllib.request.urlopen(requests)

        # 回调状态
        callback = response.read()
        # print(callback)
        return callback



if __name__ == '__main__':
    pass
    # 调用函数,需要传两个参数,contents,mobile
    # 列如:contents="哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈",mobile="13612238280",password=abc123
    # contents = "13612238280"
    # # 参数错误也会受理
    # mobile = "11"
    #
    # send_sms = REST()
    # send_sms.run(contents, mobile)
    # # # 这是获取回调的办法
    # print(send_sms.run(contents, mobile))
    # b'{"status":"10","batchId":["6280326589989011768"],"errorCode":"AllSuccess"}'

