"""WebAna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from WebAna.views import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^index/$',index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^startscan/$',startscan),
    url(r'^checkflag/$',checkflag),
    url(r'^start_analysis_link/$',start_analysis_link),
    url(r'^get_analysis_link/$',get_analysis_link),
    url(r'^badcode/$',badcode),
    url(r'^start_scansrc/$',start_scansrc),
    url(r'^get_scansrc_status/$',get_scansrc_status),
    url(r'^removeCaches/$',removeCaches),
    url(r'^watchsys/$',watchsys),
    (r'bower_components/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    (r'views/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH1}),
    (r'images/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH2}),
    (r'styles/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH3}),
    (r'scripts/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH4}),
)
