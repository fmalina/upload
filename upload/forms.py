from django.conf import settings
from django import forms
from upload.models import File, make_dir
from upload import app_settings
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
import os

# soft rotation and flip codes
TRANSPOSITION_CODES = {
    0: [],
    1: [],
    2: [Image.FLIP_LEFT_RIGHT],
    3: [Image.ROTATE_180],
    4: [Image.FLIP_TOP_BOTTOM],
    5: [Image.FLIP_TOP_BOTTOM, Image.ROTATE_270],
    6: [Image.ROTATE_270],
    7: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_270],
    8: [Image.ROTATE_90],
}


class FileForm(forms.ModelForm):
    file_data = forms.FileField(required=False)
    pos = forms.CharField(required=False, initial=1, widget=forms.HiddenInput())

    class Meta:
        model = File
        exclude = ('col',)
        widgets = {'alt': forms.TextInput({'placeholder': 'Enter caption'})}

    def url(self):
        return self.instance.url()

    def path(self):
        return self.instance.path()

    def save(self, col, request):
        if self.is_valid():
            file_label = [x.id_for_label for x in self.visible_fields()
                          if x.id_for_label.endswith('file_data')][0]
            file_data = request.FILES.get(file_label[3:])
            f = self.cleaned_data.get('id')
            alt = self.cleaned_data.get('alt', '')
            pos = self.cleaned_data.get('pos')
            if not pos:  # pos 0 sets the main image in col.save()
                pos = 1
            if f:
                src = f.path()
                f.col = col
                dst = f.path()
                f.alt = alt
                f.pos = pos
                if src != dst:  # move file from tmp to collection folder
                    make_dir(dst)
                    try:
                        os.rename(src, dst)
                    except FileNotFoundError:
                        pass
            elif file_data:
                f = File(col=col, alt=alt, fn=file_data.name[:60])
                f.save()
                y = handle_file(file_data, f)
                if not y and f:
                    f.delete()
                    return False
            return f


def handle_file(data, file_obj):
    path = file_obj.path()
    make_dir(path)
    f = open(path, 'wb+')
    try:
        for chunk in data.chunks():
            f.write(chunk)
    except AttributeError:  # no chunks
        f.write(data)
    f.close()
    os.chmod(path, 0o777)
    try:
        im = Image.open(path)
    except IOError:
        os.remove(path)
        return False

    def fff(size): return Image.new('RGB', size, app_settings.UPLOAD_FILL_ALPHA)

    # add white background to semi-transparent images
    if app_settings.UPLOAD_FILL_ALPHA and im.mode in ('RGBA', 'P'):
        bg = fff(im.size)
        im = Image.composite(im.convert('RGB'), bg, im.convert('RGBA'))
    # process soft rotation
    if im.mode == 'RGB':
        orientation = 1
        try:
            exif = im._getexif() or {}
        except AttributeError:
            exif = {}
        for k in exif.keys():
            if k in TAGS.keys() and TAGS[k] == 'Orientation':
                orientation = int(exif[k])
        for transposition in TRANSPOSITION_CODES[orientation]:
            im = im.transpose(transposition)
    # convert all to RGB for JPEG
    if im.mode != 'RGB':
        im.convert('RGB')
    # larger canvas for images too small
    x, y = im.size
    MIN = 180
    if x < MIN or y < MIN:
        w, h = x, y
        if w < MIN: w = MIN
        if h < MIN: h = MIN
        x1 = w//2 - x//2
        y1 = h//2 - y//2
        im2 = fff((w, h))
        im2.paste(im, (x1, y1, x1+x, y1+y))
        im = im2
    # downsize large images
    down_to_x, down_to_y = app_settings.UPLOAD_DOWNSIZE_TO
    if x > down_to_x or y > down_to_y:
        im.thumbnail(app_settings.UPLOAD_DOWNSIZE_TO, Image.ANTIALIAS)
    # crop off white edges
    if x > MIN and y > MIN:
        invert_im = ImageOps.invert(im)
        im = im.crop(invert_im.getbbox())
    im.save(path, 'JPEG')
    file_obj.w, file_obj.h = im.size
    file_obj.save()
    return im


class CropForm(forms.Form):
    x, y, width, height = [forms.IntegerField(widget=forms.HiddenInput())] * 4
