from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from upload.tests.test_views import index, album
from upload.views_post import FilesEditView

urlpatterns = [
    url(r'^$', index),
    url(r'^post$', FilesEditView.as_view(), name="post"),
    url(r'^(?P<pk>[0-9]+)$', album),
    url(r'^upload/', include('upload.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
