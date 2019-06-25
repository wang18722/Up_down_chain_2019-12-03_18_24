from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views
# from rest_framework.routers import DefaultRouter

urlpatterns = [
    # 关键字设置
    url(r'^info/$',views.RemindInfoViews.as_view()),

    # 关键字/地址匹配的内容
    # url(r"^search/$",views.BidsSearchViewSet.as_view()),

    # 单篇文章的获取
    # url(r"^article/(?P<pk>\d+)/$",views.BidsSinglearticle.as_view()),

    # 收藏操作
    # url(r"^collection/$",views.ArticledetailViews.as_view())

    # 快搜
    # url(r'^fastseek/$',views.BidssearchView.as_view()),

    # 快搜历史
    url(r'^history/$',views.KeywordView.as_view())

]

router = DefaultRouter()
router.register("fastseeks", views.BidsSearchView, base_name="fastseeks_search")
router.register("search", views.BidsSearchViewSet, base_name="BidsSearchViewSet_search")
router.register("fastseek", views.RetrieveIndexView, base_name="fastseek_search")
router.register("casual", views.Casual_Go, base_name="Casual_search")
urlpatterns += router.urls
