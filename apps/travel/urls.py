from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^$', views.index),
     url(r'^logout$', views.logout),
     url(r'^travels$', views.travels),
     url(r'^travels/destination/(?P<trip_id>\d+)$', views.trip),
     url(r'^travels/add$', views.add),
     url(r'^travels/destination/(?P<trip_id>\d+)/join$', views.join),
     url(r'^register$', views.register),
     url(r'^login$', views.login),
     url(r'^travels/create$', views.create),
     url(r'^travels/destination/(?P<id>\d+)/destroy$', views.destroy),
     url(r'^travels/destination/(?P<id>\d+)/leave$', views.leave),
]