from django.conf.urls import url

from Visual import views

app_name='Visual'
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^weibo/$',views.weibo,name='weibo'),
    url(r'^weibo/(?P<id>[0-9]+)/$',views.show_weibo,name='show_weibo'),
    url(r'^search_user/$',views.search_user,name='search_user'),
    url(r'^listing/$',views.UserView.as_view(),name='listing'),
    url(r'^listing_weibo/$',views.weiboView.as_view(),name='listing_weibo'),
    url(r'^show/(?P<id>[0-9]+)/$',views.show,name='show'),
    url(r'^search_weibo/$',views.search_weibo,name='search_weibo'),
    url(r'^comments/(?P<post_id>[0-9]+)/$',views.comments,name='comments'),
]