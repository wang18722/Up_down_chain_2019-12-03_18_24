from django.conf.urls import url

from . import views


urlpatterns = [

    # 用户登陆;
    url(r"^$", views.UserOuthsUrl.as_view(), name="用户登陆"),

    # 获取用户信息;
    url(r'^users/$', views.UserOpenIdViews.as_view())
]
