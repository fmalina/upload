from django.conf.urls import url
from upload.views import upload, edit

urlpatterns = [
    url(r'^upload$', upload),
    url(r'^(?P<pk>[0-9]+)/upload$', upload),
    url(r'^crop/(?P<pk>[0-9]+)$', edit, name='crop'),
    url(r'^rotate/(?P<pk>[0-9]+)/(?P<angle>(90|270))$', edit, name='rotate'),
]
