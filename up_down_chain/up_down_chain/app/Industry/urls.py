from rest_framework.routers import DefaultRouter
from . import views
urlpatterns = [

]

# #首页搜索
router = DefaultRouter()
router.register("search", views.SearchView, base_name="Enterprise_search")
urlpatterns += router.urls
# 精准检索
router.register("precise", views.PreciseRetrievalView, base_name="precise_search")
urlpatterns += router.urls