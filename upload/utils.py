from django.conf import settings
from django.utils.http import urlquote
from django.contrib.auth import REDIRECT_FIELD_NAME

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

