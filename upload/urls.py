from django.conf.urls.defaults import patterns, include, url
import settings

urlpatterns = patterns('upload.views',
    url(r'^$', 'index'),
    url(r'^post$', 'post', name="post"),
    url(r'^upload$', 'upload'),
    url(r'^(?P<slug>[A-Za-z0-9]+)$', 'ad'),
    url(r'^(?P<slug>[A-Za-z0-9]+)/upload$', 'upload'),
    url(r'^(?P<slug>[A-Za-z0-9]+)/edit$', 'post', name="edit"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )