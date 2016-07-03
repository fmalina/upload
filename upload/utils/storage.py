from django.conf import settings


def img_url(file_id, uid):
    folder = 'tmp'
    if uid:
        # ext3 subfolders limit workaround
        ext3_shard = int(uid) // (32000-2)
        folder = '%s/%s' % (ext3_shard, uid)
    if file_id is not None:
        return settings.MEDIA_URL + folder + '/%s.jpg' % file_id
    return ''
