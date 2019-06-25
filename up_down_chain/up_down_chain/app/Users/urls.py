from django.conf.urls import url

from . import views

urlpatterns = [
    #短信发送样板
    url(r'^send$', views.SmsCodeView.as_view()),
    #发送短信
    url(r'^sms$', views.SMSView.as_view()),
    #获取模板
    url(r'^template/', views.TemplateView.as_view()),
    #模板增删
    url(r'^change$', views.CreateDeleteTemplateView.as_view()),
    # url(r'^change/', views.CreateDeleteTemplateView.as_view()),
    #企业认证
    url(r'^certification/', views.EnterpriseCertificationView.as_view()),
    #审核
    url(r'^updates/reviewers/$', views.ReviewerView.as_view()),
    #获取
    url(r'^get/update/reviewer/$', views.GetReviewerView.as_view()),
    # 短信精准
    url(r'^accurate/', views.AccurateView.as_view()),
    #获取消费信息
    url(r'^info/money/', views.BalanceInfoView.as_view()),
    #认证支付
    url(r'^certifications/pay/', views.PayCertificationView.as_view()),



]