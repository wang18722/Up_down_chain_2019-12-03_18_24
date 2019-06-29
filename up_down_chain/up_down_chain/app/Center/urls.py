from django.conf.urls import url

from . import views

urlpatterns = [
    #个人中心
    url(r'^user/info', views.UserCenterView.as_view()),
    #自画像
    url(r'^self/portrait', views.SelfPortraitView.as_view()),


]