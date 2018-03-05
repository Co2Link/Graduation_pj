from django.urls import path
from django.conf.urls import url
from . import views

app_name='blog' #视图函数命名空间  将name与其他应用中区分开来
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
]
