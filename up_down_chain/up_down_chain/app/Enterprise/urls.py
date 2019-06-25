from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    url(r'^info/', views.IndexView.as_view()),
    # 基本信息
    url(r'^basic/', views.BasicInformationView.as_view()),
    # url(r'^dimen/$', views.RecommendedView.as_view()),
    # 下链行业返回url
    url(r'^industry/$', views.IndexIndustryView.as_view()),
    # 上连省份数据
    url(r'^up/industrys/$', views.UpIndexIndustryView.as_view()),
    # 列表数据
    url(r'^list/', views.ListView.as_view()),
    # 换一批
    url(r'^batch/inbatch/', views.InBatchView.as_view()),
    # 默认首页
    # url(r'^default/function/$', views.DefaultView.as_view()),
    # 我推荐
    url(r'^recommended/function/$', views.RecommendedView.as_view()),
    # 定时器
    url(r'^column/$', views.ColumnView.as_view()),
    # 访问数和推荐数
    url(r'^searchfunction/', views.SearchFunctionView.as_view()),
    # 单一行业获取数据
    url(r'^single/', views.SingleIndustryView.as_view()),

    # 省份
    url(r'^areas/', views.AreasViews.as_view()),
    # 行业
    url(r'^industrys/', views.EnterpriseMarketingView.as_view())

]

