from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),

#BELT EXAM URLS HERE:
    url(r'^friend/(?P<id>\d+)$', views.friend),
    url(r'^unfriend/(?P<id>\d+)$', views.unfriend),
    url(r'^profile/(?P<id>\d+)$', views.profile),
]