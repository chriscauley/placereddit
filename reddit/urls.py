from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

s = "(?P<slug>[\w\d\-\_]+)"
wxh = "(?P<width>\d+)x(?P<height>\d+)"
ex = "(?P<extension>\.\w+)?"

urlpatterns = patterns(
  'reddit.views',
  url(r'^$',redirect_to, {'url': '/r/featured/'}),
  url(r'^%s/(?P<template>how_to_use|how_it_works|list_of_subreddits|django)?/?$'%s,'index',name='index'),
  url(r'^%s/%s%s$'%(s,wxh,ex),'image',name='image'),
  url(r'^%s/%s_[1,2,3]?\d%s$'%(s,wxh,ex),'image',name='image'),
)
