from django.conf.urls import url
from . import views
# from rest_framework.routers import DefaultRouter

urlpatterns = [
    # 关键字设置
    url(r'^info/$',views.RemindInfoViews.as_view()),

    # 关键字/地址匹配的内容
    url(r"^search/(?P<areas>.+)/(?P<keywords>.+)/$",views.BidsSearchViewSet.as_view()),

    # 单篇文章的获取
    url(r"^article/(?P<pk>\d+)/$",views.ArticledetailViews.as_view())
]


# router = DefaultRouter()
# router.register('search', views.BidsSearchViewSet, base_name='bids_search')
#
# urlpatterns += router.urls