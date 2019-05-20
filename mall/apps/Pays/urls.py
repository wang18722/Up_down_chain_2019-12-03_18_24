from django.conf.urls import url

from Pays import views



urlpatterns = [

    # 支付下单及请求
    url(r'^wechatPay$', views.WechatPay.as_view()),
    # 授权请求
    url(r'^auth/$', views.AuthView.as_view()),
    # 之前的授权回调页面
    url(r'^index$', views.GetInfoView.as_view()),
    # 调起支付后返回结果的回调页面
    url(r'^success$', views.success),

    url(r'task/$',views.PayBaseInfo.as_view())
]
