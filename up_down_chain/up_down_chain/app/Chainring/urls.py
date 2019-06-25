

from django.conf.urls import url

from Chainring import views



urlpatterns = [
        #首页url
        url(r'^indexs/$', views.ChainRingView.as_view()),
        url(r'^focus/', views.FocusView.as_view()),



]
