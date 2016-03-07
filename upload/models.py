from django.db.models import Model, CharField, ForeignKey, IntegerField
import os, settings
UPLOAD_ROOT = settings.MEDIA_ROOT[:-1]

class User(Model): # user/site
    slug = CharField(max_length=20, unique=True)
    
    def __unicode__(self):
        return self.slug

class Ad(Model): # ad/page
    user = ForeignKey(User)
    slug = CharField(max_length=20, unique=True)
    
    def get_absolute_url(self):
        return '/'+ self.slug

class File(Model):
    ad  = ForeignKey(Ad, blank=True, null=True)
    no  = IntegerField(blank=True, null=True, editable=False) # old ID
    pos = IntegerField(blank=True, null=True) # order position
    alt = CharField('alternative text' , max_length=60, blank=True)
    fn  = CharField('original filename', max_length=60, blank=True)
    
    def url(self, uid=False):
        folder = '/tmp'
        if self.ad: uid = self.ad.user_id
        if uid:
            ext3_sub = uid / (32000-2) # subfolders limit workaround
            folder = '/%s/%s' % (ext3_sub, uid)
        if self.id:
            n = self.id
            if self.no != None: n = self.no # legacy url
            return folder + '/%s.jpg' % n
        return ''
    
    def delete(self, *args, **kwargs):
        path = UPLOAD_ROOT + self.url()
        try: os.unlink(path)
        except: pass
        super(File, self).delete(*args, **kwargs)
    
    class Meta:
        db_table = 'images' # or 'files'