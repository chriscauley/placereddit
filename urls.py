from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
  '',
  url(r'^admin/', include(admin.site.urls)),
  url(r'^r/', include('reddit.urls')),
  url(r'^nsfw/',include('reddit.urls')),
  url(r'^$','reddit.views.redirect', {'url': '/r/featured/'}),
  url(r'^test_page/$','reddit.views.test_page'),
)

if settings.DEBUG:
  urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT,
         'show_indexes': True}),
    )
