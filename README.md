# Upload with photo rotate/crop tools and python backend

Reusable web app to work with file and photo uploads.

- contains vanilla JS multifile drag and drop upload UI with instant
thumbnails and progress bars, using the W3C File API see
[upload/static/upload.js](upload/upload.js)
- python/PIL backend for upload, cropping, autocrop and rotation of photos
- seamless integration into Django projects
- image cropping UI (uses jQuery)

Thumbnails are generated using python PIL/Pillow using easy-thumbnails
or compatible thumbnail app such as sorl-thumbnails.

Generic foreign key allows to associate uploads with any content object
(user profile, staff profile, message, album, page, gallery, listing).
This way uploaded files can be grouped into collections too.


## Installation (into a Django project)

To get the latest version from GitHub
```bash
pip3 install -e git+git://github.com/fmalina/upload.git#egg=upload
```
Add `upload` to your `INSTALLED_APPS`
```python
INSTALLED_APPS = (
    ...,
    'upload',
)
```
Configure your settings to suit, see upload/app_settings.py. You can use
the collection model provided.

Add the `upload` URLs to your `urls.py`
```python
urlpatterns = [
    ...
    url(r'^upload/', include('upload.urls')),
]
```
Create your tables
```bash
./manage.py migrate upload
```
## Usage

### Setup a collection

This app supports multiple collections (or your custom model) with
multiple files in each collection.

### Add files

Drag and drop upload photos and files into your application. Files can
have alternative description and are orderable.

## Remarks

Upload shines best for sites that need ability to upload photo
galleries.

It will automatically shard the storage folder so as to not hit ext3
subfolder limit (\~32000 folders).

Included is also a backup management tool to sync/download publicly
uploaded files from server to a local machine.

### Integration

Simple integration works out of the box.

To upload files for any model taking advantage of generic foreign key,
link:
```html
<a href="{% url 'upload_edit' app_label model(lower) object_id %}">Upload</a>
```
So a profile picture upload link might look like:
```html
<a href="{% url 'upload_edit' 'auth' 'user' request.user.pk %}">Upload</a>
```
An important view to reuse or use as inspiration in a custom integration
is `views_post.FilesEditView`.

### Example settings
```python
import os

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = APP_ROOT + STATIC_URL
MEDIA_ROOT = STATIC_ROOT + 'media/'
```
### Access control

You can control editing access by implementing `is_editable_by` method
on your collection model such as:
```python
def is_editable_by(self, user):
    if user.pk == self.user_id or user.is_staff:
        return True
    return False
```
The above ensures that a collection is only editable by its user and
staff.
