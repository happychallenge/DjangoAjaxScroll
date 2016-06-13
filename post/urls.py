"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.post_list, name='post_list'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^detail/(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^update/(?P<post_id>[0-9]+)/$', views.post_update, name='post_update'),
    url(r'^delete/(?P<post_id>[0-9]+)/$', views.post_delete, name='post_delete'),
    url(r'^search/$', views.post_search, name='post_search'),                       #Ajax 
    url(r'^likes/(?P<post_id>[0-9]+)/$', views.post_likes, name='post_likes'),      #Ajax 
    url(r'^list/ajax/$', views.post_list_ajax, name='post_list_ajax'),      #Ajax 
]
