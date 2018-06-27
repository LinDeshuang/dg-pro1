from django.conf.urls import url
from django.urls import path

from app import views


urlpatterns = [
    url(r'^index/(\d+)', views.index, name='index'),

    url(r'^index/', views.index, name='index'),

    url(r'^search/(\d+)', views.search, name='search'),

    url(r'^register', views.register, name='register'),

    url(r'^login', views.login, name='login'),

    url(r'^logout', views.logout, name='logout'),

    url(r'^myinfo', views.myinfo, name='myinfo'),

    url(r'^modifypwd', views.modifypwd, name='modifypwd'),

    url(r'^publishpage', views.publishPage, name='publishpage'),

    url(r'^publish', views.publish, name='publish'),

    url(r'^mypublish/(\d+)', views.myPublish, name='mypublish'),

    url(r'^editpublish/(\d+)', views.editPublish, name='editpublish'),

    url(r'^delpublish', views.delPublish, name='delpublish'),

    url(r'^detail/(\d+)', views.detail, name='detail'),

    url(r'^comment', views.comment, name='comment'),

    url(r'^replycomment', views.replyComment, name='replycomment'),

    url(r'^setphoto', views.setphoto, name='setphoto'),

    url(r'^getvcode', views.getVcode, name='getvcode'),

    url(r'^announce/(\d+)', views.announce, name='announce'),

]
app_name = 'app'
