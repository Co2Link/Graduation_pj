from django.conf.urls import url
from my_main import views
app_name='my_main'
urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^crawl/', views.crawl, name='crawl'),
    url(r'^clean/',views.clean,name='clean'),
]
