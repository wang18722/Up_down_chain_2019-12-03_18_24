from django.conf.urls import url

from . import views

urlpatterns = [
    # 支付回调保存
    url(r'^$',views.PufaPayment.as_view()),

    # 充值记录
    url(r'^recharge/$',views.RechargeMent.as_view()),
    # 充值钱包
    url(r"^rechargeinfo/$", views.RechargePayment.as_view()),

    url(r"task/sms/callback", views.SmsCallbackView.as_view()),


]
