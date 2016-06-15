from django.conf import settings
from django.utils.http import urlquote
from django.apps import apps
from django.contrib.auth import REDIRECT_FIELD_NAME
from upload.app_settings import UPLOAD_COLLECTION_MODEL

def get_collection_model():
    """
    Support for custom collection model
    with developer friendly validation.
    """
    try:
        app_label, model_name = UPLOAD_COLLECTION_MODEL.split('.')
    except ValueError:
        raise ImproperlyConfigured("UPLOAD_COLLECTION_MODEL must be of the"
                                   " form 'app_label.model_name'")
    collection_model = apps.get_model(app_label=app_label, model_name=model_name)
    if collection_model is None:
        raise ImproperlyConfigured("UPLOAD_COLLECTION_MODEL refers to"
                                   " model '%s' that has not been installed"
                                   % UPLOAD_COLLECTION_MODEL)
    return collection_model


def ext3_shard(uid):
    """ext3 subfolders limit workaround"""
    return int(uid) // (32000-2)


def img_url(n, uid):
    folder = settings.MEDIA_URL+'tmp'
    if uid:
        folder = settings.MEDIA_URL+'%s/%s' % (ext3_shard(uid), uid)
    if n != None:
        return folder + '/%s.jpg' % n
    return ''


def img_path(n, uid):
    if n != None:
        return settings.STATIC_ROOT + img_url(n, uid)
    return ''


def login_url(next_url, next_name=REDIRECT_FIELD_NAME):
    """ Use with care.
    There are no checks that the next_url had not been tampered with.
    """
    return '%s?%s=%s' % (settings.LOGIN_URL, next_name, urlquote(next_url))
