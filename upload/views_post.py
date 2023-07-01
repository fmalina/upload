from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms import ModelForm
from upload.forms import FileForm
from upload.models import File, Collection, get_content_object
from upload import app_settings


def get_object_form(c_type):
    """Return modelform for the GFK model"""
    model_class = c_type.model_class()

    class _ObjectForm(ModelForm):
        class Meta:
            model = model_class
            fields = []
            exclude = ['user']
    return _ObjectForm


class FilesEditView(View):
    model = Collection
    template_name = "upload/post.html"

    def file_set(self):
        return generic_inlineformset_factory(File, FileForm)

    def post(self, request, app_label=None, model=None, object_id=None):
        c_type, obj = get_content_object(app_label, model, object_id)

        data = [request.POST]
        if request.FILES:
            data.append(request.FILES)

        form = get_object_form(c_type)(*data, instance=obj)
        files = self.file_set()(*data, instance=obj)

        if form.is_valid():
            if not obj:
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
            for file_form in files.forms:
                f = file_form.save(obj, request)
                if file_form.cleaned_data.get('DELETE', False):
                    f.delete()
                elif f:
                    f.content_object = obj
                    f.save()
            return redirect(obj)
        return

    def get(self, request, app_label=None, model=None, object_id=None):
        c_type, obj = get_content_object(app_label, model, object_id)

        form = get_object_form(c_type)(instance=obj)
        files = self.file_set()(instance=obj)

        if not obj:
            url = reverse('xhr_up')
        elif obj:
            url = reverse('xhr_up_gfk', kwargs={'app_label': app_label,
                                                'model': model,
                                                'object_id': object_id})

        return render(request, self.template_name, {
            'form': form,
            'images': files,
            'instance': obj,
            'xhr_upload_url': url,
            'upload_imap_enabled': app_settings.UPLOAD_IMAP_ENABLED,
            'upload_imap_email': app_settings.UPLOAD_IMAP_EMAIL
        })
