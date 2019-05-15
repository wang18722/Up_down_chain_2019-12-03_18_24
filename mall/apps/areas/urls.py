from django.conf.urls import url
from . import views
urlpatterns = [
    # 推送地址
    url(r'^info/$',views.AreasViews.as_view(),name="推送地址")

]