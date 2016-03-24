from django.shortcuts import get_object_or_404, render, redirect
from django.forms.models import BaseInlineFormSet, inlineformset_factory as inline
from upload.models import File, Collection
from upload.forms import FileForm
from upload.tests.test_forms import CollectionForm


def index(request):
    return render(request, 'index.html', {
        'collections': Collection.objects.all()})


def collection(request, pk):
    col = get_object_or_404(Collection, pk=pk)
    images = col.file_set.order_by('no')
    return render(request, 'collection.html', {
        'col': col,
        'images': images
    })


def file_set():
    return inline(Collection, File, FileForm, BaseInlineFormSet,
                  extra=4, can_delete=True, max_num=30)


def post(request, pk=None):
    col = None; data = (None,)
    if pk:
        col = get_object_or_404(Collection, pk=pk)
    if request.POST and request.FILES:
        data = (request.POST, request.FILES)
    if request.POST:
        data = (request.POST,)
    form = CollectionForm(*data, instance=col)
    files = file_set()(*data, instance=col)
    if form.is_valid():
        col = form.save()
        for file_form in files.forms:
            f = file_form.save(col, request)
            if file_form.cleaned_data.get('DELETE', False):
                f.delete()
            elif f:
                f.save()
        return redirect(col)
    return render(request, 'post.html', {
        'col': col,
        'form': form,
        'images': files
    })
