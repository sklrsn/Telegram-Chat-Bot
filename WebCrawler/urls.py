from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^store/', views.store_data),
]
