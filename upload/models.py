from django.db import models
from django.apps import apps
from django.conf import settings
from upload import app_settings
import os.path
import os


class File(models.Model):
    """ Single file, its original filename, collection, order position in it
    and it's short text alternative.
    """
    col = models.ForeignKey(app_settings.UPLOAD_COLLECTION_MODEL,
                            blank=True, null=True)
    no = models.IntegerField('legacy #',
                             blank=True, null=True, editable=False)
    pos = models.IntegerField('order position', blank=True, null=True)
    alt = models.CharField(max_length=60, blank=True)
    fn = models.CharField('original filename', max_length=60,
                          blank=True, editable=False)

    def url(self):
        folder = 'tmp'
        if self.col_id:
            # ext3 subfolders limit workaround
            ext3_shard = int(self.col_id) // (32000-2)
            folder = '%s/%s' % (ext3_shard, self.col_id)
        return settings.MEDIA_URL + folder + '/%s.jpg' % self.pk

    def path(self):
        return app_settings.UPLOAD_ROOT + self.url()

    def delete(self, *args, **kwargs):
        path = self.path()
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
    One can therefore attach uploads to any one model
    such as Article, Album, Gallery, Pics, Photos, FilesFolder.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def is_editable_by(self, user):
        """Permission check that each collection_model has to implement.
        Here only collection owner or trusted staff users can upload and edit.
        """
        if user.pk == self.user_id or user.is_staff:
            return True
        return False

    def crop(self):
        """One can define conditional thumbnail cropping rules
        in their swappable collection_model based on type of collection.
        E.g.: .crop() can return "smart" for landscapes or ",0" for mugshots.
        See cropping options docs of the thumbnailing app.
        """
        return 'smart'

    def get_absolute_url(self):
        return '/%s' % self.pk


def get_collection_model():
    """
    Support for custom collection model
    with developer friendly validation.
    """
    try:
        app_label, model_name = app_settings.UPLOAD_COLLECTION_MODEL.split('.')
    except ValueError:
        raise ImproperlyConfigured("UPLOAD_COLLECTION_MODEL must be of the"
                                   " form 'app_label.model_name'")
    collection_model = apps.get_model(app_label=app_label,
                                      model_name=model_name)
    if collection_model is None:
        raise ImproperlyConfigured("UPLOAD_COLLECTION_MODEL refers to"
                                   " model '%s' that has not been installed"
                                   % UPLOAD_COLLECTION_MODEL)
    return collection_model


def make_dir(path):
    try:
        dirname = os.path.dirname(path)
        os.makedirs(dirname)
    except FileExistsError:
        pass
