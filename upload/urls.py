from django.conf.urls import url
from upload.views import upload, edit
from upload.views_post import FilesEditView

urlpatterns = [
    # XHR handler to upload files
    url(r'^$',
        upload, name='xhr_up'),
    # XHR handler for files in existing collection
    url(r'^(?P<pk>[0-9]+)$',
        upload, name='xhr_up_col'),
    # XHR handler for files associated with any object via generic foreign key
    url(r'^(?P<app_label>[a-z]+)-(?P<model>[a-z]+)/(?P<object_id>[0-9]+)$',
        upload, name='xhr_up_gfk'),

    # Post collection
    url(r'^post$',
        FilesEditView.as_view(), name="upload_col"),

    # Edit existing collection
    url(r'^(?P<pk>[0-9]+)/edit$',
        FilesEditView.as_view(), name='upload_col_edit'),

    # Edit files with generic foreign key relation
    url(r'^(?P<app_label>[a-z]+)-(?P<model>[a-z]+)/(?P<object_id>[0-9]+)/edit$',
        FilesEditView.as_view(), name='upload_gfk_edit'),

    # Crop and rotate images
    url(r'^crop/(?P<pk>[0-9]+)$', edit, name='crop'),
    url(r'^rotate/(?P<angle>(90|270))/(?P<pk>[0-9]+)$', edit, name='rotate'),
]
