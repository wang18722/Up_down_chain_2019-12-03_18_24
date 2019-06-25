# import re
#
# from django import forms
# # from django.forms import widgets
# from django.core.exceptions import ValidationError  # 钩子模块
# # from .models import User
# from .models import EnterpriseCertificationInfo
#
#
# class UserForm(forms.Form):
#     # openid = forms.CharField()
#     # wechat_nickname = forms.CharField()
#     # wechat_sex = forms.CharField()
#     # wechat_headimgUrl = forms.ImageField()
#     name = forms.CharField()
#     code = forms.CharField()
#     contacts = forms.CharField()
#     phone = forms.CharField()
#     identity_status = forms.CharField()
#     administrator_status = forms.CharField()
#     user_id = forms.CharField()
#     avatar = forms.ImageField()
#     company_id = forms.CharField()
#
#
#     # class Meta:
#     #     model = EnterpriseCertificationInfo
#     #     fields = "__all__"
#     #     error_messages = {
#     #         'avatar': {
#     #             'invalid_image': '请上传正确格式的图片！'
#     #         }
#     #     }
#
#
#     # 局部钩子---查看是否已经存在企业用户
#     def clean_username(self):
#         name = self.cleaned_data.get('name')
#         user_new = EnterpriseCertificationInfo.objects.filter(name=name).first()
#         if not user_new:
#             return name  # 如果没有那么直接返回干净数据
#         else:
#             raise ValidationError('该企业用户已注册')  # 错误提示语法
#
#     def clean_code(self):
#         mobile = self.cleaned_data.get('code')
#         mobile_new = EnterpriseCertificationInfo.objects.filter(code=mobile).first()
#         if not mobile_new:
#             return mobile  # 如果没有那么直接返回干净数据
#         else:
#             raise ValidationError('该统一社会信用代码已存在')  # 钩子错误提示语法
#
#     def clean_code1(self):
#         value = self.cleaned_data['code']
#         mobile_regex = re.compile(r'^[0-9A-Z]{18}$')
#         if not mobile_regex.match(value):
#             raise ValidationError('统一社会信用代码格式错误')
#         return value
#
#     def clean_phone(self):
#         value = self.cleaned_data['phone']
#         mobile_regex = re.compile(r'^1[3578][0-9]{9}$')
#         if not mobile_regex.match(value):
#             raise ValidationError('手机号码格式错误')
#         return value
#     #
#     #
