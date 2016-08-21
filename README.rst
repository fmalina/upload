HTML5 upload with photo rotate/crop tools and Django backend
============================================================

.. image:: https://travis-ci.org/fmalina/upload.svg?branch=master
    :target: https://travis-ci.org/fmalina/upload

A reusable Django app to work with photo and file uploads.
Extracted from FlatmateRooms photo upload feature
https://www.FlatmateRooms.co.uk/post (please don't save if testing)

- contains native JavaScript multifile drag and drop upload UI with instant thumbnails and progress bars, see `upload/static/upload.js <https://github.com/fmalina/upload/blob/master/upload/static/upload/upload.js>`_
- python/PIL backend for upload, cropping, autocrop and rotation of photos
- seamless integration into Django projects
- image cropping UI (uses jQuery)

Thumbnails are generated using python PIL/Pillow using easy-thumbnails or
compatible thumbnailing application such as sorl-thumbnails.

Uploaded files are grouped into sortable collections, the collection model
is swappable via settings, so uploaded files can be grouped to an Album, Page,
Gallery, Listing etc.

Generic foreign key allows to associate uploads with any content object (user
profile, staff profile, message) while also supporting swappable collections.

upload.js builds on the following HTML5 demos:
http://html5demos.com/dnd-upload
http://html5demos.com/file-api
upload.js uses the W3C File API 
https://dev.opera.com/articles/w3c-file-api/

Installation (into a Django project)
------------------------------------

To get the latest version from GitHub

::

    pip install -e git+git://github.com/fmalina/upload.git#egg=upload

Add ``upload`` to your ``INSTALLED_APPS``

::

    INSTALLED_APPS = (
        ...,
        'upload',
    )

Configure your settings to suit, see upload/app_settings.py.
You can use the collection model provided or plug your own using
settings.py:

::

    UPLOAD_COLLECTION_MODEL = 'yourcastleapp.Castle'

Add the ``upload`` URLs to your ``urls.py``

::

    urlpatterns = [
        ...
        url(r'^upload/', include('upload.urls')),
    ]

Create your tables

::

    ./manage.py migrate upload


Usage
-----

Setup a collection
~~~~~~~~~~~~~~~~~~
This app supports multiple collections (or your custom model) with
multiple files in each collection.

Add files
~~~~~~~~~
Drag and drop upload photos and files into your application.
Files can have alternative description and are orderable.

Remarks
-------
Upload shines best for sites that need ability to upload photo galleries.

It will automatically shard the storage folder so as to not hit ext3 subfolder
limit (~32000 folders).

Included is also a backup management tool to sync/download publicly uploaded
files from server to a local machine.

Integration
~~~~~~~~~~~
Simple integration works out of the box. To upload files to collections link:
``<a href="{% url 'upload_col_edit' pk=org.pk %}">Upload</a>``
from your editing interface. ``org`` being an instance of your collection model.

Or to upload files for any model taking advantage of generic foreign key, link:
``<a href="{% url 'upload_gfk_edit' app_label model(lowercase) object_id %}">``

Therefore a profile picture upload link might look like so:
``<a href="{% url 'upload_gfk_edit' 'auth' 'user' request.user.pk %}">...</a>``

An important view to reuse or use as inspiration in a custom integration is
``views_post.FilesEditView``.

Contribute
----------
Fork it and send your pull request. File and issue. Mention on your blog,
tweet, status update. Tell your dev friends and mention when complaining
to sites that have poor upload features.

Flask reusability rewrite would be a welcome contribution, if you need another
server backend such as for MongoDB or PHP please fork off and let me know
how you get on.
