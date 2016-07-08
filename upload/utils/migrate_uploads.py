"""
Migrate files from old storage model using:

    user_id based ext3_shard / user_id / file_id(or legacy number).jpg

to new storage model

    col_id based ext3_shard / col_id / file_id .jpg

where ext3_shard is a workaround for ext3 filesystem 32k subfolders limit

    ext3_shard = int(col_id) // (32000-2)
"""
from upload.utils.spoonfeed import spoonfeed
from upload import app_settings


def from_path(f):
    uid = f.col.user_id
    ext3_shard = int(uid) // (32000-2)
    folder = '%s/%s/' % (ext3_shard, uid)
    n = f.id
    if f.no is not None:  # legacy url
        n = f.no
    return app_settings.UPLOAD_ROOT + settings.MEDIA_URL +\
           folder + '%s.jpg' % n


def move_file(f):
    # TODO
    from_path = from_path(f)
    to_path = f.path()
    mv(from_path, to_path)


spoonfeed(File.objects, move_file)
