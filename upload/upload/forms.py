from django.forms import ModelForm, FileField, HiddenInput, CharField
from upload.models import Ad, File, UPLOAD_ROOT
import os, os.path, Image

class AdForm(ModelForm):
    class Meta:
        model = Ad

class FileForm(ModelForm):
    file_data = FileField(required=False)
    pos = CharField(required=False, widget=HiddenInput())
    class Meta:
        model = File
    
    def url(self):
        return self.instance.url()
    
    def save(self, ad, request):
        if self.is_valid():
            file_label = [x.id_for_label for x in self.visible_fields()
                       if x.id_for_label.endswith('file_data')][0]
            file_data = request.FILES.get(file_label[3:])
            f = self.cleaned_data.get('id')
            alt = self.cleaned_data.get('alt', '')
            try: pos = int(self.cleaned_data.get('pos', ''))
            except: pos = None
            if f:
                src = UPLOAD_ROOT + f.url()
                f.ad = ad
                dst = UPLOAD_ROOT + f.url()
                f.alt = alt
                f.pos = pos
                if src != dst: # move file from tmp to user folder
                    try: os.makedirs(os.path.dirname(dst))
                    except: pass
                    try: os.rename(src, dst)
                    except: pass
            elif file_data:
                f = File(ad=ad, alt=alt, fn=file_data.name[:60])
                f.save()
                y = handle_file(file_data, f)
                if not y and f:
                    f.delete()
                    return False
            return f

def handle_file(data, file_obj, uid=False):
    path = UPLOAD_ROOT + file_obj.url(uid)
    try: os.makedirs(os.path.dirname(path))
    except: pass
    f = open(path, 'wb+')
    try:
        for chunk in data.chunks():
            f.write(chunk)
    except AttributeError: # no chunks
        f.write(data)
    f.close()
    try:
        orig = Image.open(path)
        x, y = orig.size
        if x > 1024 or y > 768: # only resize images too large
            orig.thumbnail((768, 1024), Image.ANTIALIAS)
        orig.save(path)
        return True
    except IOError:
        os.remove(path)
        return False