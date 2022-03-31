from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from upload import app_settings
from datetime import datetime
import os.path
import os


class File(models.Model):
    """with original filename, collection GFK, order and alt text"""
    no = models.IntegerField('legacy #',
                             blank=True, null=True, editable=False)
    pos = models.IntegerField('order position', blank=True, null=True)
    w = models.IntegerField('width', blank=True, null=True)
    h = models.IntegerField('height', blank=True, null=True)
    alt = models.CharField(max_length=60, blank=True)
    fn = models.CharField('original filename', max_length=60,
                          blank=True, editable=False)
    hash = models.CharField(max_length=40, blank=True)

    # generic foreign key allows to associate uploads with any content object
    content_object = GenericForeignKey()
    # nullable to support XHR uploads before collection instance is saved
    content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                     on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField(blank=True, null=True)

    updated_at = models.DateTimeField(default=datetime.now, editable=False)
    created_at = models.DateTimeField(default=datetime.now, editable=False)

    def base_path(self):
        folder = 'tmp'
        if self.object_id:
            # ext3 sub-folders limit workaround
            ext3_shard = int(self.object_id) // (32000-2)
            folder = f'{ext3_shard}/{self.object_id}'
        return f'{folder}/{self.pk}.jpg'

    def path(self):
        return app_settings.UPLOAD_ROOT + self.base_path()

    def url(self):
        return settings.MEDIA_URL + self.base_path() +\
               '?' + self.short_hash()

    def short_hash(self):
        return self.hash[:6]

    def delete(self, *args, **kwargs):
        path = self.path()
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass
        super(File, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(File, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.url()

    class Meta:
        ordering = ['content_type', 'object_id', 'pos']


class Collection(models.Model):
    """
    Test collection model. One can attach uploads to any model using GFK
    but implementing following methods on that model may be necessary
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_set = GenericRelation(File)

    def is_editable_by(self, user):
        """
        Permission check that each collection_model has to implement.
        Here only collection owner or trusted staff users can upload and edit.
        """
        if user.pk == self.user_id or user.is_staff:
            return True
        return False

    def crop(self):
        """
        Thumbnail cropping rules each collection_model needs in place.
        One can define conditional rules based on type of collection.
        E.g.: .crop() can return "smart" for landscapes or ",0" for profile pics.
        See cropping options docs of the thumbnail app.
        """
        return 'smart'

    def get_absolute_url(self):
        return f'/{self.pk}'


def get_content_object(app_label, model, object_id):
    """For use in views"""
    if app_label and model and object_id:
        content_type = get_object_or_404(ContentType, app_label=app_label,
                                         model=model)
        return content_type.get_object_for_this_type(pk=object_id)
    return


def make_dir(path):
    try:
        dirname = os.path.dirname(path)
        os.makedirs(dirname)
    except FileExistsError:
        pass
