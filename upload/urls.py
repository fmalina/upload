from django.conf.urls import url
from django.conf import settings
from upload.views import index, post, ad, upload, edit

urlpatterns = [
    url(r'^$', index),
    url(r'^post$', post, name="post"),
    url(r'^(?P<pk>[0-9]+)$', ad),
    url(r'^upload$', upload),
    url(r'^(?P<pk>[0-9]+)/upload$', upload),
    url(r'^crop/(?P<pk>[0-9]+)$', edit, name='crop'),
    url(r'^rotate/(?P<pk>[0-9]+)/(?P<angle>(90|270))$', edit, name='rotate'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   ]
