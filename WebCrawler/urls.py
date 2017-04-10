from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/', views.search_content, name="search_content"),
    url(r'^store/', views.store_data, name="store_data"),
    url(r'^store_webhook/', views.store_data_web_hook, name="store_data_web_hook"),
]
