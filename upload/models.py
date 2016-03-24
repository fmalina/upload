from django.db import models
from django.conf import settings
from upload.utils import img_url
from upload.app_settings import UPLOAD
import os, os.path


class File(models.Model):
    col = models.ForeignKey(UPLOAD['collection_model'], blank=True, null=True)
    no  = models.IntegerField('legacy #', blank=True, null=True, editable=False)
    pos = models.IntegerField('order position', blank=True, null=True)
    alt = models.CharField(max_length=60, blank=True)
    fn  = models.CharField('original filename', max_length=60, blank=True, editable=False)

    def url(self, uid=False):
        if not uid and self.col:
            uid = self.col.user_id
        n = None
        if self.id:
            n = self.id
            if self.no != None: # legacy url
                n = self.no
        return img_url(n, uid)

    def path(self, uid=False):
        return UPLOAD['media_root'] + self.url(uid)

    def delete(self, *args, **kwargs):
        path = UPLOAD['media_root'] + self.url()
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass
        super(File, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return self.url()

    class Meta:
        ordering = ['col', 'pos']


class Collection(models.Model):
    """Swappable using collection_model setting.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def crop(self):
        return ''

    def get_absolute_url(self):
        return '/'+ self.pk


def make_dir(path):
    try:
        dirname = os.path.dirname(path)
        os.makedirs(dirname)
    except FileExistsError:
        pass
