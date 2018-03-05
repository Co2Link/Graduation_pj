from django.conf.urls import url
from my_main import views
urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^crawl/', views.crawl, name='crawl'),
]
