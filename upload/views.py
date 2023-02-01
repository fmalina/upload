from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from upload.forms import handle_file, save_sizes, CropForm
from upload.models import File, get_content_object
from upload.utils.imaging import meets_min_size
from upload import app_settings
from PIL import Image


def is_permitted(user, obj):
    if obj is None:
        return True
    if obj and hasattr(obj, 'is_editable_by') and obj.is_editable_by(user):
        return True
    return False


def upload(request, app_label=None, model=None, object_id=None):
    data = request.FILES.get('file')
    if data:
        f = File(fn=data.name[:60])
        c_type, obj = get_content_object(app_label, model, object_id)
        if not is_permitted(request.user, obj):
            return HttpResponse('not permitted')
        f.content_object = obj
        f.save()
        im = handle_file(data, f)
        if not im:
            f.delete()
        else:
            c = {'id': f.id, 'path': f.path(), 'crop': ''}
            if f.content_object:
                c['crop'] = getattr(f.content_object, 'crop', 'smart')
            if not meets_min_size(im, app_settings.UPLOAD_MIN_SIZE):
                f.delete()
                return HttpResponse('small')
            ok = render_to_string('upload/xhr.js', c)
            return HttpResponse(ok)
    return HttpResponse('error')


def edit(request, pk, angle=0):
    """Handle cropping and rotation even before signup"""
    f = get_object_or_404(File, pk=pk)
    obj = f.content_object
    if not is_permitted(request.user, obj):
        return HttpResponse('not permitted')
    p = f.path()
    try:
        im = Image.open(p)
    except IOError:
        p = p.replace('tmp', str(f.object_id))
        im = Image.open(p)
    # pass collection defined cropping onto thumbnail
    # e.g. smart crop v. middle crop from top
    crop = ''
    if obj and hasattr(obj, 'crop'):
        crop = obj.crop()
    if angle:  # handle rotation
        im.transpose({
            '90': Image.ROTATE_90,
            '270': Image.ROTATE_270
        }[angle]).save(p)
        save_sizes(f)
        return HttpResponse('rotated')
    else:  # or handle cropping
        form = CropForm(request.POST or None)
        if form.is_valid():
            d = form.cleaned_data
            # get starting position and cutout size
            x, y, w, h = d['x'], d['y'], d['x']+d['width'], d['y']+d['height']
            # crop image and save
            im.crop((x, y, w, h)).save(p)
            save_sizes(f)
        return render(request, 'upload/crop.html', {
            'img': f,
            'crop': crop,
            'form': form
        })
