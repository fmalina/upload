from django.conf.urls import url
from upload.views import upload, edit

urlpatterns = [
    url(r'^$', upload, name='upload'),
    url(r'^(?P<pk>[0-9]+)$', upload, name='upload_edit'),
    url(r'^crop/(?P<pk>[0-9]+)$', edit, name='crop'),
    url(r'^rotate/(?P<angle>(90|270))/(?P<pk>[0-9]+)$', edit, name='rotate'),
]
