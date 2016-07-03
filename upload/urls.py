from django.conf.urls import url
from upload.views import upload, edit
from upload.views_post import FilesEditView

urlpatterns = [
    # XHR handler to upload files
    url(r'^$',
        upload,
        name='upload'),
    # XHR handler for files in existing collection
    url(r'^(?P<pk>[0-9]+)$',
        upload,
        name='upload_edit'),

    # Post collection
    url(r'^post$',
        FilesEditView.as_view(),
        name="upload_col"),
    # Edit existing collection
    url(r'^(?P<pk>[0-9]+)/edit$',
        FilesEditView.as_view(),
        name='upload_col_edit'),

    # Crop and rotate images
    url(r'^crop/(?P<pk>[0-9]+)$', edit, name='crop'),
    url(r'^rotate/(?P<angle>(90|270))/(?P<pk>[0-9]+)$', edit, name='rotate'),
]
