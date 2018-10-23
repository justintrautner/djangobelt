from django.conf.urls import url
from . import views         
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^add$', views.add),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^myaccount/(?P<id>\d+)$', views.myaccount),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^like/(?P<id>\d+)$', views.like),
    url(r'^dislike/(?P<id>\d+)$', views.dislike),


    



]    