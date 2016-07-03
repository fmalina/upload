from django.conf import settings
from upload import app_settings


def ext3_shard(uid):
    """ext3 subfolders limit workaround"""
    return int(uid) // (32000-2)


def img_url(n, uid):
    folder = settings.MEDIA_URL+'tmp'
    if uid:
        folder = settings.MEDIA_URL+'%s/%s' % (ext3_shard(uid), uid)
    if n is not None:
        return folder + '/%s.jpg' % n
    return ''
