from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from upload.forms import handle_file, CropForm
from upload.models import File, get_collection_model
from upload.utils import login_url
from PIL import Image

Col = get_collection_model()


def upload(request, pk=False):
    data = request.FILES.get('file')
    res = 'error'
    uid = False
    if data:
        if request.user.is_authenticated():
            uid = request.user.pk
        f = File(fn=data.name[:60])
        if pk:
            col = get_object_or_404(Col, pk=pk)
            f.col = col
            uid = col.user_id
            # only collection owner or trusted staff users can upload
            if not request.user.is_staff and not request.user.pk == col.user_id:
                return HttpResponse('not permitted')
        f.save()
        y = handle_file(data, f, uid)
        if y:
            c = {'id': f.id, 'path': f.path(uid), 'crop': ''}
            if f.col: c['crop'] = f.col.crop
            res = render_to_string('upload/xhr.js', c)
        else: f.delete()
    return HttpResponse(res)


def edit(request, pk, angle=0):
    """
    Handle cropping and rotation even before users signup.
    """
    f = get_object_or_404(File, pk=pk)
    uid = False
    if request.user.is_authenticated():
        uid = request.user.pk
    if f.col:
        uid = f.col.user_id
        if not request.user.is_authenticated():
            return redirect(login_url(request.path_info))
        # only collection owner or trusted staff users can edit
        if not request.user.is_staff and not request.user.pk == uid:
            return HttpResponse('not permitted')
    p = f.path(uid)
    try:
        im = Image.open(p)
    except IOError:
        p = p.replace('tmp', str(request.user.pk))
        im = Image.open(p)
    # pass collection defined cropping onto thumbnail
    # e.g. smart crop v. middle crop from top
    crop=''
    if f.col:
        crop = f.col.crop()
    if angle: # handle rotation
        im.transpose({
            '90': Image.ROTATE_90,
            '270': Image.ROTATE_270
        }[angle]).save(p)
        return render(request, 'upload/reload-thumbnails.html', {
            'img': f,
            'user_id': uid, 
            'crop': crop
        })
    else: # or handle cropping
        form = CropForm(request.POST or None)
        if form.is_valid():
            d = form.cleaned_data
            # get starting position and cutout size 
            x, y, w, h = d['x'], d['y'], d['x']+d['width'], d['y']+d['height']
            # crop image and save
            im.crop((x, y, w, h)).save(p)
        return render(request, 'upload/crop.html', {
            'img': f,
            'img_url': f.url(uid),
            'img_path': f.path(uid),
            'crop': crop,
            'form': form
        })
