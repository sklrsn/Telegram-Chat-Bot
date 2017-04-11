from django.conf.urls import url
from Explorer import views

urlpatterns = [
    url(r'^exploreByUserName/', views.ExploreByUsername.as_view(), name="ExploreByUsername"),
    url(r'^exploreByDate/', views.ExploreByDate.as_view(), name="ExploreByDate"),
    url(r'^exploreByKeyword/', views.ExploreByKeyword.as_view(), name="ExploreByKeyword")
]
