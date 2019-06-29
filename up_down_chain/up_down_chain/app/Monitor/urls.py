from django.conf.urls import url

from . import views

urlpatterns = [
    #短信发送样板
    url(r'^main/monitor/', views.MonitorUserView.as_view()),
    url(r'^online/user/', views.OnlineUserView.as_view()),

]