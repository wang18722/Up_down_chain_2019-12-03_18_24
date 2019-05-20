from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # 关键字设置
    url(r'^info/$',views.RemindInfoViews.as_view()),

    # 关键字/地址匹配的内容
    url(r"^search/(?P<areas>.+)/(?P<keywords>.+)/$",views.BidsSearchViewSet.as_view()),

    # 单篇文章的获取
    url(r"^article/$",views.BidsSinglearticle.as_view()),

    # 收藏操作
    url(r"^collection/$",views.ArticledetailViews.as_view())

]


router = DefaultRouter()
router.register('search', views.SKUSearchViewSet, base_name='bids_search')

urlpatterns += router.urls