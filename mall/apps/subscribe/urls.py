from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # 关键字设置
    url(r'^info/$',views.RemindInfoViews.as_view())
]


router = DefaultRouter()
router.register('search', views.SKUSearchViewSet, base_name='bids_search')

urlpatterns += router.urls