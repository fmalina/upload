from django.urls import path, re_path
from upload.views import upload, edit
from upload.views_post import FilesEditView

MODEL_PATH = '^(?P<app_label>[a-z]+)-(?P<model>[a-z]+)/'
OBJECT_ID = '(?P<object_id>[0-9]+)'
edit_col = FilesEditView.as_view()

urlpatterns = [
    # XHR handler to upload files
    path('', upload, name='xhr_up'),
    # XHR handler for files in existing collection
    # associated with any object via generic foreign key
    re_path(f'{MODEL_PATH}{OBJECT_ID}$', upload, name='xhr_up_gfk'),
    # create/update collection of files with generic foreign key relation
    re_path(f'{MODEL_PATH}post$', edit_col, name='upload'),
    re_path(f'{MODEL_PATH}{OBJECT_ID}/edit$', edit_col, name='upload_edit'),
    # Crop and rotate images
    path('crop/<int:pk>', edit, name='crop'),
    re_path(r'^rotate/(?P<angle>(90|270))/(?P<pk>[0-9]+)$', edit, name='rotate'),
]
