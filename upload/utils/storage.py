from django.conf import settings


def img_url(n, uid):
    folder = 'tmp'
    if uid:
        # ext3 subfolders limit workaround
        ext3_shard = int(uid) // (32000-2)
        folder = '%s/%s' % (ext3_shard, uid)
    if n is not None:
        return settings.MEDIA_URL + folder + '/%s.jpg' % n
    return ''
