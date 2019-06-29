"""up_down_chain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #首页
    url(r'^index/', include('Enterprise.urls')),

    url(r'chainring/', include('Chainring.urls')),
    #企业认证
    url(r'^users/', include('Users.urls')),
    #用户
    url(r'^oauth/', include('oauth.urls')),
    #
    url(r'^industry/', include('Industry.urls')),

    #
    # url(r'auths/', obtain_jwt_token, name='auths'),
    # 支付
    url(r'^pay/',include('Pays.urls')),
    # 推送订阅
    url(r'^subscribe/',include('Subseribe.urls')),

    #触客
    url(r'^contact/',include('Contact.urls')),
#监控后台
    url(r'^monitor/',include('Monitor.urls')),
    #个人中心
    url(r'^center/',include('Center.urls')),

]
