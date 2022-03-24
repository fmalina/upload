HTML5 upload with photo rotate/crop tools and Django backend
============================================================

.. image:: https://travis-ci.org/fmalina/upload.svg?branch=master
    :target: https://travis-ci.org/fmalina/upload

A reusable Django app to work with photo and file uploads.

- contains vanilla JS multifile drag and drop upload UI with instant thumbnails and progress bars,
see `upload/static/upload.js <upload/upload.js>`_
- python/PIL backend for upload, cropping, autocrop and rotation of photos
- seamless integration into Django projects
- image cropping UI (uses jQuery)

Thumbnails are generated using python PIL/Pillow using easy-thumbnails or
compatible thumbnail app such as sorl-thumbnails.

Generic foreign key allows to associate uploads with any content object (user
profile, staff profile, message, album, page, gallery, listing).
This way uploaded files can be grouped into collections too.

upload.js builds on the following HTML5 demos:
http://html5demos.com/dnd-upload
http://html5demos.com/file-api
upload.js uses the W3C File API 
https://dev.opera.com/articles/w3c-file-api/

Installation (into a Django project)
------------------------------------

To get the latest version from GitHub

::

    pip3 install -e git+git://github.com/fmalina/upload.git#egg=upload

Add ``upload`` to your ``INSTALLED_APPS``

::

    INSTALLED_APPS = (
        ...,
        'upload',
    )

Configure your settings to suit, see upload/app_settings.py.
You can use the collection model provided.

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
Simple integration works out of the box.

To upload files for any model taking advantage of generic foreign key, link:

::

    <a href="{% url 'upload_edit' app_label model(lower) object_id %}">Upload</a>

So a profile picture upload link might look like:

::

    <a href="{% url 'upload_edit' 'auth' 'user' request.user.pk %}">Upload</a>

An important view to reuse or use as inspiration in a custom integration is
``views_post.FilesEditView``.

Example settings
~~~~~~~~~~~~~~~~

::

    import os
    
    APP_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'))

    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = APP_ROOT + STATIC_URL
    MEDIA_ROOT = STATIC_ROOT + 'media/'

Access control
~~~~~~~~~~~~~~
You can control editing access by implementing ``is_editable_by`` method
on your collection model such as:

::

    def is_editable_by(self, user):
        if user.pk == self.user_id or user.is_staff:
            return True
        return False

The above ensures that a collection is only editable by its user and staff.

Contribute
----------
File issues. Fork and send pull requests. Tell developers implementing uploads.


Dual Licensing
--------------

Commercial license
~~~~~~~~~~~~~~~~~~
If you want to use Upload to develop and run commercial projects and applications, the Commercial license is the appropriate license. With this option, your source code is kept proprietary.

Once purchased, you are granted a commercial BSD style license and all set to use Upload in your business.

`Small Team License (£350) <https://unilexicon.com/fm/pay.html?amount=350&msg=Upload_Team_License>`_
Small Team License for up to 8 developers

`Organization License (£1200) <https://unilexicon.com/fm/pay.html?amount=1200&msg=Upload_Organisation_License>`_
Commercial Organization License for Unlimited developers

Open source license
~~~~~~~~~~~~~~~~~~~
If you are creating an open source application under a license compatible with the GNU GPL license v3, you may use Upload under the terms of the GPLv3.
