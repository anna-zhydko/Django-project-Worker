from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('search', views.search, name='search'),
    path('search', views.index, name='search'),
]