from django.urls import path, re_path
from upload.views import upload, edit
from upload.views_post import FilesEditView

urlpatterns = [
    # XHR handler to upload files
    path('', upload, name='xhr_up'),
    # XHR handler for files in existing collection
    path('<int:pk>', upload, name='xhr_up_col'),
    # XHR handler for files associated with any object via generic foreign key
    re_path(r'^(?P<app_label>[a-z]+)-(?P<model>[a-z]+)/(?P<object_id>[0-9]+)$',
            upload, name='xhr_up_gfk'),

    # Post collection
    path('post', FilesEditView.as_view(), name="upload_col"),

    # Edit existing collection
    path('<int:pk>/edit', FilesEditView.as_view(), name='upload_col_edit'),

    # Edit files with generic foreign key relation
    re_path(r'^(?P<app_label>[a-z]+)-(?P<model>[a-z]+)/(?P<object_id>[0-9]+)/edit$',
            FilesEditView.as_view(), name='upload_gfk_edit'),

    # Crop and rotate images
    path('crop/<int:pk>', edit, name='crop'),
    re_path(r'^rotate/(?P<angle>(90|270))/(?P<pk>[0-9]+)$', edit, name='rotate'),
]
