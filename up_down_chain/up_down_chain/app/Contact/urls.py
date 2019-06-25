from django.conf.urls import url
from . import views

urlpatterns = [
    #AI自动营销
    url(r'^ai/marketing', views.AiMarketingView.as_view()),

# 触客文章
    url(r'^artic/$',views.TouchArticlesViews.as_view()),

    # 触客单篇文章
    url(r'^artic/(?P<pk>\d+)/content/$',views.ObtainTouchArticlesViews.as_view()),

    # 触客文章评论
    url(r'^comment/$',views.CommentsOnArticlesViews.as_view()),

    # 点赞
    url(r'^thumbs/$',views.ThumbsUpViews.as_view())

]