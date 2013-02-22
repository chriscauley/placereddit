from django.conf.urls import patterns, include, url

s = "(?P<subreddit>[\w\d\-\_]+)(?P<nsfw>/nsfw)?"
wxh = "(?P<width>\d+)x(?P<height>\d+)"
ex = "(?P<extension>\.\w+)?"

urlpatterns = patterns(
  'reddit.views',
  url(r'^$','index',name='index'),
  url(r'^%s/$'%s,'index',name='index'),
  url(r'^%s/%s%s$'%(s,wxh,ex),'image',name='image'),
  url(r'^%s/%s_\d%s$'%(s,wxh,ex),'image',name='image'),
)
