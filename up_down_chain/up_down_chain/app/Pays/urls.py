from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.PufaPayment.as_view()),
    #url(r"task/sms/callback",views.SmsCallback.as_view())
    # 充值
    url(r'^recharge/$',views.RechargeMent.as_view()),
    url(r"task/sms/callback", views.SmsCallbackView.as_view())
]
