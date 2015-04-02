from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import BaseInlineFormSet, inlineformset_factory as inline
from django.http import HttpResponse
from upload.models import Ad, User, File
from upload.forms import AdForm, FileForm, handle_file

def index(request):
    return render(request, 'index.html', {'ads': Ad.objects.all()})

def ad(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    images = ad.file_set.order_by('no')
    return render(request, 'ad.html', {'ad': ad, 'images': images})

def file_set():
    return inline(Ad, File, FileForm, BaseInlineFormSet, extra=4, can_delete=True, max_num=30)

def post(request, slug=None):
    ad = None; data = (None,)
    if slug:
        ad = get_object_or_404(Ad, slug=slug)
    if request.POST and request.FILES:
        data = (request.POST, request.FILES)
    if request.POST:
        data = (request.POST,)
    form = AdForm(*data, instance=ad)
    files = file_set()(*data, instance=ad)
    if form.is_valid():
        ad = form.save()
        for file_form in files.forms:
            f = file_form.save(ad, request)
            if file_form.cleaned_data.get('DELETE', False):
                f.delete()
            elif f:
                f.save()
        return redirect(ad)
    return render(request, 'post.html', {
        'ad': ad,
        'form': form,
        'images': files
    })

def upload(request, slug=False):
    data = request.FILES.get('file')
    res = 'error'
    if data:
        f = File(fn=data.name[:60])
        if slug:
            ad = get_object_or_404(Ad, slug=slug)
            f.ad = ad
        f.save()
        uid = False
        # if request.user.loggedin():
        #     uid = request.user.id
        y = handle_file(data, f, uid)
        if y: res = "{'id':%s,'url':'%s'}" % (f.id, f.url(uid))
        else: f.delete()
    return HttpResponse(res)