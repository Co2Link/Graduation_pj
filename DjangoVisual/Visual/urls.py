from django.conf.urls import url

from Visual import views

app_name='Visual'
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^search_user/$',views.search_user,name='search_user'),
]