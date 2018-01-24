from django.conf import settings
from django.conf.urls import  url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^levels/$', views.levels, name='levels'),
    url(r'^basico/$', views.basico, name='basico'),
    url(r'^intermedio/$', views.levels, name='intermedio'),
    url(r'^avanzado/$', views.levels, name='avanzado'),
]
