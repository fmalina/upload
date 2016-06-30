from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from upload.tests.test_views import index, album

urlpatterns = [
    url(r'^$', index),
    url(r'^(?P<pk>[0-9]+)$', album),
    url(r'^upload/', include('upload.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
