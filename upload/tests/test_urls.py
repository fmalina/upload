from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from upload.tests.test_views import index, post, collection

urlpatterns = [
    url(r'^$', index),
    url(r'^post$', post, name="post"),
    url(r'^(?P<pk>[0-9]+)$', collection),
    url('', include('upload.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
